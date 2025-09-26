"""Ultra-lean single optimized ORB+FVG strategy (backtest + live MT5).
Defaults: 30m OR (09:30 NY), retest after BOS + 3-candle FVG, FVG>=0.25 ATR14, SL zone extreme±5p, TP 2R.
CSV or MT5 data for backtest; mock synthetic fallback if none present. One long + one short per day.
Usage (examples):
    Backtest: python orb_final_optimized.py --mode backtest --symbol USDCAD --data-folder data --export-trades trades.csv
    Live (signals only): python orb_final_optimized.py --mode live --symbol USDCAD
    Live (auto): python orb_final_optimized.py --mode live --symbol USDCAD --enable-trading --risk-percent 0.5
"""
from __future__ import annotations

import argparse
import math
import os
import time as time_mod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple, Dict, Any, Set

import numpy as np
import pandas as pd
import pytz

try:  # Optional MetaTrader5
    import MetaTrader5 as mt5  # type: ignore
except Exception:  # noqa: BLE001
    mt5 = None  # type: ignore


@dataclass
class Config:
    symbol: str = "USDCAD"
    tz_name: str = "America/New_York"
    session_open_h: int = 9
    session_open_m: int = 30
    or_minutes: int = 30
    fvg_min_atr_frac: float = 0.25
    atr_period: int = 14
    sl_buffer_pips: float = 5.0
    risk_reward: float = 2.0
    poll_interval: int = 30
    enable_trading: bool = False
    order_type: str = "market"  # or 'limit'
    risk_percent: float = 0.5
    trade_log_csv: str = "final_trades.csv"
    signal_log_csv: str = "final_live_signals.csv"
    allow_weekend: bool = False
    pip_scale: float = 0.0001
    mt5_backfill_days: Optional[int] = None
    # Costs
    spread_pips: float = 0.0
    slippage_pips: float = 0.0
    commission_per_lot: float = 0.0
    # Exports
    export_equity: Optional[str] = None


def mt5_ready() -> bool:
    if mt5 is None:
        return False
    try:
        return mt5.initialize()
    except Exception:  # noqa: BLE001
        return False


def load_csv(path: str) -> Optional[pd.DataFrame]:
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        df.columns = [c.lower() for c in df.columns]
        if "time" not in df.columns:
            return None
        if not np.issubdtype(df["time"].dtype, np.datetime64):
            if np.issubdtype(df["time"].dtype, np.number):
                df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
            else:
                df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.set_index("time").sort_index()
        return df[["open", "high", "low", "close"]]
    except Exception:  # noqa: BLE001
        return None


def generate_mock(days: int = 90, seed: int = 33):
    rng = np.random.default_rng(seed)
    start = datetime(2024, 1, 2, tzinfo=timezone.utc)
    periods = days * 288
    idx = pd.date_range(start, periods=periods, freq="5min", tz=timezone.utc)
    base = 1.31 + np.cumsum(rng.normal(0, 0.00022, size=periods))
    o = base
    h = o + rng.random(size=periods) * 0.00035
    l = o - rng.random(size=periods) * 0.00035
    c = o + rng.normal(0, 0.00013, size=periods)
    m5 = pd.DataFrame({"open": o, "high": h, "low": l, "close": c}, index=idx)
    m15 = m5.resample("15min").agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    return m5, m15


def fetch_mt5_history(symbol: str, days: int) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    if mt5 is None:
        return None, None
    end = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = end - timedelta(days=days)
    def conv(r):
        if r is None:
            return None
        df = pd.DataFrame(r)
        if df.empty:
            return None
        df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
        df = df.set_index('time').sort_index()
        return df[['open','high','low','close']]
    m5 = conv(mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, start, end))
    m15 = conv(mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, start, end))
    return m5, m15


def fetch_recent(symbol: str, timeframe: int, bars: int) -> Optional[pd.DataFrame]:
    if mt5 is None:
        return None
    r = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if r is None:
        return None
    df = pd.DataFrame(r)
    if df.empty:
        return None
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    df = df.set_index('time').sort_index()
    return df[['open','high','low','close']]


def atr(df: pd.DataFrame, period: int) -> pd.Series:
    pc = df['close'].shift(1)
    tr = pd.concat([(df['high'] - df['low']), (df['high'] - pc).abs(), (df['low'] - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(period, min_periods=1).mean()


def detect_fvg3(df: pd.DataFrame, i: int) -> Optional[Tuple[float, float, bool]]:
    if i < 2:
        return None
    c_now = df.iloc[i]
    c_prev2 = df.iloc[i - 2]
    if c_now.low > c_prev2.high:
        return (c_prev2.high, c_now.low, True)
    if c_now.high < c_prev2.low:
        return (c_now.high, c_prev2.low, False)
    return None


def opening_range(m5: pd.DataFrame, day_mid_local: datetime, cfg: Config) -> Tuple[float, float, datetime, datetime]:
    or_start_local = day_mid_local + timedelta(hours=cfg.session_open_h, minutes=cfg.session_open_m)
    or_end_local = or_start_local + timedelta(minutes=cfg.or_minutes)
    or_start_utc = or_start_local.astimezone(timezone.utc)
    or_end_utc = or_end_local.astimezone(timezone.utc)
    slc = m5[(m5.index >= or_start_utc) & (m5.index < or_end_utc)]
    if slc.empty:
        return math.nan, math.nan, or_start_utc, or_end_utc
    return float(slc.high.max()), float(slc.low.min()), or_start_utc, or_end_utc


def evaluate_day(day_mid_local: datetime, m5: pd.DataFrame, cfg: Config, atr_series: pd.Series) -> List[Dict[str, Any]]:
    or_high, or_low, _, or_end_utc = opening_range(m5, day_mid_local, cfg)
    if math.isnan(or_high):
        return []
    after = m5[m5.index >= or_end_utc]
    if after.empty:
        return []
    trades: List[Dict[str, Any]] = []

    # Long branch
    long_candidate = None
    for i in range(len(after)):
        if i < 2:
            continue
        row = after.iloc[i]
        hi = float(row.high)
        prev_hi = float(after.iloc[i - 1].high)
        bos_up = hi > or_high and prev_hi <= or_high
        if not bos_up:
            continue
        fvg = detect_fvg3(after, i)
        if not fvg or not fvg[2]:
            continue
        atr_val = atr_series.loc[after.index[i]] if after.index[i] in atr_series.index else math.nan
        gap_size = fvg[1] - fvg[0]
        if math.isnan(atr_val) or atr_val <= 0 or gap_size < cfg.fvg_min_atr_frac * atr_val:
            continue
        # Demand: last red prior
        demand = None
        for j in range(i - 1, -1, -1):
            c = after.iloc[j]
            if c.close < c.open:
                demand = c
                break
        if demand is None:
            break
        zone_low = float(demand.low)
        zone_high = float(demand.high)
        # Retest
        forward = after.iloc[i + 1 :]
        entry_price = entry_time = None
        for k in range(len(forward)):
            r2 = forward.iloc[k]
            if float(r2.low) <= zone_high:
                entry_price = zone_high
                entry_time = forward.index[k]
                break
        if entry_price is None:
            break
        sl = zone_low - cfg.sl_buffer_pips * cfg.pip_scale
        risk = entry_price - sl
        if risk <= 0:
            break
        tp = entry_price + cfg.risk_reward * risk
        long_candidate = dict(direction='long', entry_time=entry_time, entry=entry_price, sl=sl, tp=tp,
                              breakout_extreme=hi, breakout_time=after.index[i], zone_high=zone_high, zone_low=zone_low,
                              or_high=or_high, or_low=or_low)
        break

    # Short branch
    short_candidate = None
    for i in range(len(after)):
        if i < 2:
            continue
        row = after.iloc[i]
        lo = float(row.low)
        prev_lo = float(after.iloc[i - 1].low)
        bos_down = lo < or_low and prev_lo >= or_low
        if not bos_down:
            continue
        fvg = detect_fvg3(after, i)
        if not fvg or fvg[2]:
            continue
        atr_val = atr_series.loc[after.index[i]] if after.index[i] in atr_series.index else math.nan
        gap_size = fvg[0] - fvg[1]
        if math.isnan(atr_val) or atr_val <= 0 or gap_size < cfg.fvg_min_atr_frac * atr_val:
            continue
        supply = None
        for j in range(i - 1, -1, -1):
            c = after.iloc[j]
            if c.close > c.open:
                supply = c
                break
        if supply is None:
            break
        zone_low = float(supply.low)
        zone_high = float(supply.high)
        forward = after.iloc[i + 1 :]
        entry_price = entry_time = None
        for k in range(len(forward)):
            r2 = forward.iloc[k]
            if float(r2.high) >= zone_low:
                entry_price = zone_low
                entry_time = forward.index[k]
                break
        if entry_price is None:
            break
        sl = zone_high + cfg.sl_buffer_pips * cfg.pip_scale
        risk = sl - entry_price
        if risk <= 0:
            break
        tp = entry_price - cfg.risk_reward * risk
        short_candidate = dict(direction='short', entry_time=entry_time, entry=entry_price, sl=sl, tp=tp,
                               breakout_extreme=lo, breakout_time=after.index[i], zone_high=zone_high, zone_low=zone_low,
                               or_high=or_high, or_low=or_low)
        break

    for cand in [long_candidate, short_candidate]:
        if cand:
            trades.append(simulate_trade(cand, m5, cfg))
    return trades


def simulate_trade(trade: Dict[str, Any], m5: pd.DataFrame, cfg: Config) -> Dict[str, Any]:
    if trade['entry_time'] not in m5.index:
        idx_pos = m5.index.searchsorted(trade['entry_time'])
        if idx_pos >= len(m5.index):
            trade['exit'] = trade['entry']
            trade['exit_time'] = trade['entry_time']
            trade['exit_reason'] = 'NO_DATA'
            trade['r_mult'] = 0.0
            return trade
        trade['entry_time'] = m5.index[idx_pos]
    entry_loc = m5.index.get_loc(trade['entry_time'])
    horizon = m5.iloc[entry_loc + 1 : entry_loc + 600]
    direction = trade['direction']
    exit_price = exit_time = None
    exit_reason = None
    for ts, bar in horizon.iterrows():
        h = float(bar.high)
        l = float(bar.low)
        if direction == 'long':
            if l <= trade['sl']:
                exit_price, exit_time, exit_reason = trade['sl'], ts, 'SL'
                break
            if h >= trade['tp']:
                exit_price, exit_time, exit_reason = trade['tp'], ts, 'TP'
                break
        else:
            if h >= trade['sl']:
                exit_price, exit_time, exit_reason = trade['sl'], ts, 'SL'
                break
            if l <= trade['tp']:
                exit_price, exit_time, exit_reason = trade['tp'], ts, 'TP'
                break
    if exit_price is None:
        if horizon.empty:
            exit_price = trade['entry']
            exit_time = trade['entry_time']
            exit_reason = 'NO_HORIZON'
        else:
            last = horizon.iloc[-1]
            exit_price = float(last.close)
            exit_time = horizon.index[-1]
            exit_reason = 'TIME'
    trade['exit'] = exit_price
    trade['exit_time'] = exit_time
    trade['exit_reason'] = exit_reason
    if direction == 'long':
        raw_r = (exit_price - trade['entry']) / (trade['entry'] - trade['sl'])
    else:
        raw_r = (trade['entry'] - exit_price) / (trade['sl'] - trade['entry'])
    risk_price = abs(trade['entry'] - trade['sl'])
    pip = cfg.pip_scale
    spread_r = (cfg.spread_pips * pip) / risk_price if cfg.spread_pips > 0 and risk_price > 0 else 0.0
    slip_r = (cfg.slippage_pips * pip) / risk_price if cfg.slippage_pips > 0 and risk_price > 0 else 0.0
    commission_r = (cfg.commission_per_lot / 100.0) if cfg.commission_per_lot > 0 else 0.0
    net_r = raw_r - (spread_r + slip_r + commission_r)
    trade['raw_r'] = raw_r
    trade['cost_r'] = (spread_r + slip_r + commission_r)
    trade['r_mult'] = net_r
    trade['hold_minutes'] = (exit_time - trade['entry_time']).total_seconds() / 60 if exit_time else 0
    return trade


def aggregate(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not trades:
        return dict(trades=0, win_rate=0, avg_r=0, expectancy=0, pf=0, max_dd=0, median_hold=0, tp_hit=0)
    rs = np.array([t['r_mult'] for t in trades])
    wins = rs[rs > 0]
    losses = rs[rs <= 0]
    win_rate = (rs > 0).mean()
    avg_win = wins.mean() if len(wins) else 0
    avg_loss = losses.mean() if len(losses) else 0
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss
    gross_win = wins.sum() if len(wins) else 0
    gross_loss = -losses.sum() if len(losses) else 0
    pf = gross_win / gross_loss if gross_loss > 0 else (gross_win if gross_win > 0 else 0)
    eq = np.cumsum(rs)
    peak = np.maximum.accumulate(eq)
    dd = eq - peak
    max_dd = dd.min() if len(dd) else 0
    med_hold = float(np.median([t['hold_minutes'] for t in trades]))
    tp_hit = float(np.mean([t['exit_reason'] == 'TP' for t in trades]))
    return dict(trades=len(trades), win_rate=round(win_rate,4), avg_r=round(float(rs.mean()),4),
                expectancy=round(float(expectancy),4), pf=round(float(pf),3), max_dd=round(float(max_dd),2),
                median_hold=round(med_hold,1), tp_hit=round(tp_hit,4))


def run_backtest(cfg: Config, data_folder: str, export_trades: Optional[str], export_summary: Optional[str]):
    m5 = m15 = None
    if cfg.mt5_backfill_days and mt5_ready():
        m5, m15 = fetch_mt5_history(cfg.symbol, cfg.mt5_backfill_days)
    if m5 is None or m15 is None:
        m5_path = os.path.join(data_folder, f"{cfg.symbol.upper()}_M5.csv")
        m15_path = os.path.join(data_folder, f"{cfg.symbol.upper()}_M15.csv")
        m5 = load_csv(m5_path)
        m15 = load_csv(m15_path)
    mock_used = False
    if m5 is None or m15 is None:
        print("[WARN] Using mock synthetic data (not real performance)")
        m5, m15 = generate_mock()
        mock_used = True
    if cfg.symbol.upper().endswith('JPY'):
        cfg.pip_scale = 0.01
    atr_series = atr(m5, cfg.atr_period)
    tz = cfg.tz_name
    days_local = m5.index.tz_convert(tz).date
    uniq_days = sorted(set(days_local))
    all_trades: List[Dict[str, Any]] = []
    for d in uniq_days:
        local_mid = pytz.timezone(tz).localize(datetime(d.year, d.month, d.day))
        utc_start = local_mid.astimezone(timezone.utc)
        utc_end = utc_start + timedelta(days=1)
        day_slice = m5[(m5.index >= utc_start) & (m5.index < utc_end)]
        if day_slice.empty:
            continue
        all_trades.extend(evaluate_day(local_mid, day_slice, cfg, atr_series))
    summary = aggregate(all_trades)
    print("Summary:", summary)
    if mock_used:
        print("NOTE: Replace mock with real CSV or MT5 for valid evaluation.")
    df_trades = pd.DataFrame(all_trades)
    if not df_trades.empty:
        df_trades = df_trades.sort_values('exit_time')
        df_trades['cum_r'] = df_trades['r_mult'].cumsum()
        if cfg.export_equity:
            df_trades[['exit_time','cum_r']].to_csv(cfg.export_equity, index=False)
            print(f"Equity exported -> {cfg.export_equity}")
    if export_trades:
        df_trades.to_csv(export_trades, index=False)
        print(f"Trades exported -> {export_trades}")
    if export_summary:
        pd.DataFrame([summary]).to_csv(export_summary, index=False)
        print(f"Summary exported -> {export_summary}")
    return df_trades, summary


def lot_size(symbol: str, risk_amount: float, entry: float, sl: float) -> float:
    if mt5 is None:
        return 0.0
    info = mt5.symbol_info(symbol)
    if info is None:
        return 0.0
    point = info.point
    stop_points = abs(entry - sl) / point
    if stop_points <= 0:
        return 0.0
    pip_val_per_lot = info.trade_contract_size * point
    risk_per_lot = stop_points * pip_val_per_lot
    if risk_per_lot <= 0:
        return 0.0
    lots = risk_amount / risk_per_lot
    step = info.volume_step or 0.01
    vmin = info.volume_min or step
    vmax = info.volume_max or 100
    return max(vmin, min(vmax, round(lots / step) * step))


def place_order(trade: Dict[str, Any], cfg: Config):
    if mt5 is None:
        print("MT5 not loaded; skip order.")
        return
    acc = mt5.account_info()
    if acc is None:
        print("No account info.")
        return
    equity = acc.equity
    risk_amt = equity * (cfg.risk_percent / 100.0)
    lots = lot_size(cfg.symbol, risk_amt, trade['entry'], trade['sl'])
    if lots <= 0:
        print("Lot calc failed.")
        return
    tick = mt5.symbol_info_tick(cfg.symbol)
    if tick is None:
        print("No tick.")
        return
    if trade['direction'] == 'long':
        market_type = mt5.ORDER_TYPE_BUY
        limit_type = mt5.ORDER_TYPE_BUY_LIMIT
        market_price = tick.ask
        comment = 'FINAL_LONG'
    else:
        market_type = mt5.ORDER_TYPE_SELL
        limit_type = mt5.ORDER_TYPE_SELL_LIMIT
        market_price = tick.bid
        comment = 'FINAL_SHORT'
    if cfg.order_type == 'limit':
        o_type = limit_type
        action = mt5.TRADE_ACTION_PENDING
        price = trade['entry']
    else:
        o_type = market_type
        action = mt5.TRADE_ACTION_DEAL
        price = market_price
    req = dict(action=action, symbol=cfg.symbol, volume=lots, type=o_type, price=price,
               sl=trade['sl'], tp=trade['tp'], deviation=25, magic=1357911, comment=comment,
               type_time=mt5.ORDER_TIME_GTC, type_filling=mt5.ORDER_FILLING_RETURN)
    res = mt5.order_send(req)
    if res is None or res.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order fail retcode={getattr(res,'retcode',None)}")
    else:
        print(f"Order placed ticket={res.order} lots={lots} {trade['direction']}")


def append_csv(path: str, record: Dict[str, Any], uid: str):
    row = record.copy()
    row['unique_id'] = uid
    df = pd.DataFrame([row])
    if not os.path.exists(path):
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode='a', header=False, index=False)


def live_loop(cfg: Config):
    if mt5 is None or not mt5_ready():
        print("MT5 not ready; cannot run live mode.")
        return
    seen: Set[str] = set()
    tz = pytz.timezone(cfg.tz_name)
    print("Starting live loop (optimized variant)...")
    try:
        while True:
            now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
            if not cfg.allow_weekend and now_utc.weekday() >= 5:
                print("Weekend pause (5m)")
                time_mod.sleep(300)
                continue
            m5 = fetch_recent(cfg.symbol, mt5.TIMEFRAME_M5, 900)
            if m5 is None or m5.empty:
                print("No data; retry...")
                time_mod.sleep(cfg.poll_interval)
                continue
            atr_series = atr(m5, cfg.atr_period)
            local_today = now_utc.astimezone(tz).replace(hour=0, minute=0, second=0, microsecond=0)
            trades = evaluate_day(local_today, m5, cfg, atr_series)
            for t in trades:
                uid = f"{t['direction']}_{int(t['entry_time'].timestamp())}"
                if uid in seen:
                    continue
                seen.add(uid)
                print(f"Signal {t['direction']} entry={t['entry']:.5f} SL={t['sl']:.5f} TP={t['tp']:.5f}")
                append_csv(cfg.signal_log_csv, t, uid)
                if cfg.enable_trading:
                    place_order(t, cfg)
            time_mod.sleep(cfg.poll_interval)
    except KeyboardInterrupt:
        print("Live loop ended by user.")
    finally:
        if mt5:
            mt5.shutdown()


def parse_args():
    p = argparse.ArgumentParser(description="Final ORB FVG Optimized Variant")
    p.add_argument('--mode', choices=['live','backtest'], required=True)
    p.add_argument('--symbol', default='USDCAD')
    p.add_argument('--data-folder', default='data')
    p.add_argument('--mt5-backfill-days', type=int, default=None)
    p.add_argument('--export-trades', default=None)
    p.add_argument('--export-summary', default=None)
    p.add_argument('--export-equity', default=None)
    p.add_argument('--enable-trading', action='store_true')
    p.add_argument('--order-type', choices=['market','limit'], default='market')
    p.add_argument('--risk-percent', type=float, default=0.5)
    p.add_argument('--spread-pips', type=float, default=0.0)
    p.add_argument('--slippage-pips', type=float, default=0.0)
    p.add_argument('--commission-per-lot', type=float, default=0.0)
    p.add_argument('--poll-interval', type=int, default=30)
    p.add_argument('--allow-weekend', action='store_true')
    return p.parse_args()


def main():
    args = parse_args()
    cfg = Config(
        symbol=args.symbol,
        enable_trading=args.enable_trading,
        order_type=args.order_type,
        risk_percent=args.risk_percent,
        mt5_backfill_days=args.mt5_backfill_days,
        spread_pips=args.spread_pips,
        slippage_pips=args.slippage_pips,
        commission_per_lot=args.commission_per_lot,
        poll_interval=args.poll_interval,
        allow_weekend=args.allow_weekend,
        export_equity=args.export_equity,
    )
    if args.mode == 'backtest':
        run_backtest(cfg, args.data_folder, args.export_trades, args.export_summary)
    else:
        live_loop(cfg)


if __name__ == '__main__':
    main()
