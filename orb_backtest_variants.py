"""Variant Backtester for ORB + FVG + Zone Retest Strategy
===========================================================

This script provides an offline (historical) backtest harness for the live strategy
logic you supplied. It allows systematic evaluation of multiple *variant dimensions*
while keeping the core concept (Opening Range Breakout + FVG + Demand/Supply zone)
intact.

Why this file?
--------------
The repository did not contain the original `orb_new_variant_backtest.py`, and
MetaTrader5 (MT5) live data access inside this dev container is not guaranteed.
Therefore this harness:
 1. Tries to read locally supplied historical CSV data (so you can export from MT5 / TradingView).
 2. Falls back to generating mock synthetic OHLC data (clearly flagged) so the engine
    can still be validated structurally.

Provide Real Data
-----------------
Create a folder `data/` at repository root containing (UTC indexed or timestamp):
  data/USDCAD_M5.csv
  data/USDCAD_M15.csv

Expected CSV columns (case-insensitive accepted & auto-normalized):
  time, open, high, low, close, (optional volume)
Time must be either ISO8601 or integer epoch seconds. Script will parse.

Variant Dimensions Implemented
------------------------------
1. Opening Range window: 15m, 30m, 60m
2. Entry mode:
   - retest: Wait for first retest of the qualifying demand/supply zone after BOS
   - immediate: Enter at BOS candle close when FVG + BOS confirmed (no retest)
3. FVG pattern type:
   - fvg3: 3‑candle gap (c[i].low > c[i-2].high / c[i].high < c[i-2].low)
   - fvg2: 2‑candle gap (c[i].low > c[i-1].high / c[i].high < c[i-1].low)
4. Minimum FVG size filter (in ATR fractions of 5m bars): none, 0.25 ATR, 0.5 ATR
5. Stop-loss reference:
   - or_extreme: Opposite OR extreme ± buffer pips
   - zone: Beyond zone opposite edge ± buffer pips
6. Take Profit mode:
   - breakout: BOS candle extreme
   - r_mult_2: 2R
   - r_mult_3: 3R

To avoid combinatorial explosion, the default run samples a curated subset that tends to be practically distinct.
You can set EXPAND_FULL_MATRIX=True to brute force all combinations.

Performance Metrics Reported
----------------------------
Per variant key:
  trades           Total executed trades
  win_rate         Winning trades / total
  avg_r            Mean R multiple (R = (exit-entry)/(entry-SL) with sign)
  expectancy       win_rate*avg_win_r - (1-win_rate)*|avg_loss_r|
  pf               Profit factor (gross win / gross loss)
  max_dd_r         Max drawdown in R units (equity in cumulative R)
  med_hold_min     Median holding time (minutes)
  hit_tp_pct       Percent exits via TP (vs SL or other)

Real Data Disclaimer
--------------------
The synthetic fallback is ONLY for structural validation; results on mock data are meaningless for trading decisions.

Usage Examples
--------------
Run with mock fallback (if no CSV):
  python orb_backtest_variants.py --symbol USDCAD --year-filter 2024

Run specifying data folder: (ensure CSV exists)
  python orb_backtest_variants.py --data-folder data --symbol EURUSD --export results_variants.csv

Limit variants (e.g. only immediate entries):
  python orb_backtest_variants.py --entry-modes immediate

"""
from __future__ import annotations

import argparse
import itertools
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable, List, Optional, Tuple, Dict, Any

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------
# Configuration Data Classes
# ----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Variant:
    or_minutes: int            # 15, 30, 60
    entry_mode: str           # 'retest' | 'immediate'
    fvg_type: str             # 'fvg3' | 'fvg2'
    fvg_min_atr_frac: float   # 0.0, 0.25, 0.5
    sl_mode: str              # 'or_extreme' | 'zone'
    tp_mode: str              # 'breakout' | 'r_mult_2' | 'r_mult_3'

    def key(self) -> str:
        return (
            f"OR{self.or_minutes}_E{self.entry_mode}_F{self.fvg_type}_"
            f"FVGmin{self.fvg_min_atr_frac}_SL{self.sl_mode}_TP{self.tp_mode}"
        )


@dataclass
class BacktestConfig:
    symbol: str = "USDCAD"
    tz_name: str = "America/New_York"  # For session filtering
    session_open_h: int = 9
    session_open_m: int = 30
    buffer_pips: float = 5.0
    pip_scale: float = 0.0001  # Adjust automatically for JPY later
    max_days: Optional[int] = None
    year_filter: Optional[int] = None  # Only include this year if provided
    expand_full_matrix: bool = False
    # Risk management: Always 1R for analysis; monetary sizing omitted in backtest.


# ----------------------------------------------------------------------------------
# Data Loading / Preparation
# ----------------------------------------------------------------------------------


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {c: c.lower() for c in df.columns}
    df = df.rename(columns=rename_map)
    required = ["time", "open", "high", "low", "close"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    if not np.issubdtype(df["time"].dtype, np.datetime64):
        # Try parse as epoch or string
        try:
            # If numeric-like assume epoch seconds
            if np.issubdtype(df["time"].dtype, np.number):
                df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
            else:
                df["time"] = pd.to_datetime(df["time"], utc=True, errors="raise")
        except Exception as e:
            raise ValueError(f"Could not parse time column: {e}")
    df = df.set_index("time").sort_index()
    return df[["open", "high", "low", "close"]]


def load_csv_if_exists(path: str) -> Optional[pd.DataFrame]:
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        return _normalize_columns(df)
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return None


def generate_mock_data(days: int = 40, seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic trending + mean reverting intraday bars for M5/M15.
    Clearly labeled for transparency.
    """
    rng = np.random.default_rng(seed)
    start = datetime(2024, 1, 2, 0, 0, tzinfo=timezone.utc)
    periods_m5 = days * 288  # 24h * 12 bars
    idx_m5 = pd.date_range(start, periods=periods_m5, freq="5min", tz=timezone.utc)
    price = 1.34 + np.cumsum(rng.normal(0, 0.0003, size=periods_m5))
    # Build OHLC
    opens = price
    highs = opens + rng.normal(0.0002, 0.00005, size=periods_m5).clip(min=0)
    lows = opens - rng.normal(0.0002, 0.00005, size=periods_m5).clip(min=0)
    closes = opens + rng.normal(0, 0.00015, size=periods_m5)
    m5 = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes}, index=idx_m5)
    # Resample to M15
    m15 = m5.resample("15min").agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    return m5, m15


# ----------------------------------------------------------------------------------
# Indicator Helpers
# ----------------------------------------------------------------------------------


def compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"].shift(1)
    tr = pd.concat([(h - l), (h - c).abs(), (l - c).abs()], axis=1).max(axis=1)
    return tr.rolling(period, min_periods=1).mean()


def detect_fvg(df: pd.DataFrame, i: int, fvg_type: str) -> Optional[Tuple[float, float]]:
    if fvg_type == "fvg3":
        if i < 2:
            return None
        c_now = df.iloc[i]
        c_prev2 = df.iloc[i - 2]
        if c_now.low > c_prev2.high:
            return (c_prev2.high, c_now.low)  # bullish gap
        if c_now.high < c_prev2.low:
            return (c_now.high, c_prev2.low)  # bearish gap (bear ordering kept consistent later)
    elif fvg_type == "fvg2":
        if i < 1:
            return None
        c_now = df.iloc[i]
        c_prev = df.iloc[i - 1]
        if c_now.low > c_prev.high:
            return (c_prev.high, c_now.low)
        if c_now.high < c_prev.low:
            return (c_now.high, c_prev.low)
    return None


# ----------------------------------------------------------------------------------
# Core Daily Evaluation
# ----------------------------------------------------------------------------------


def evaluate_day(
    day: datetime,
    m5: pd.DataFrame,
    m15: pd.DataFrame,
    variant: Variant,
    cfg: BacktestConfig,
    atr_m5: pd.Series,
) -> List[Dict[str, Any]]:
    tz = cfg.tz_name
    # Determine local open time -> convert to UTC index lookup
    # Day here is midnight local (we will create that) OR we derive by shifting.
    # We'll convert each bar index to local to filter day range quickly.
    local_tz = pd.Timestamp(day.date()).tz_localize(tz)
    or_start_local = local_tz + timedelta(hours=cfg.session_open_h, minutes=cfg.session_open_m)
    or_end_local = or_start_local + timedelta(minutes=variant.or_minutes)
    # Convert to UTC
    or_start_utc = or_start_local.tz_convert(timezone.utc)
    or_end_utc = or_end_local.tz_convert(timezone.utc)

    # Opening range from m15 bars overlapping OR window aggregated via m5 for precision
    or_slice = m5[(m5.index >= or_start_utc) & (m5.index < or_end_utc)]
    if or_slice.empty:
        return []
    or_high = float(or_slice.high.max())
    or_low = float(or_slice.low.min())

    after = m5[m5.index >= or_end_utc]
    if after.empty:
        return []

    results: List[Dict[str, Any]] = []
    # We will allow at most one long + one short per day (matching live logic style) for simplicity.

    # Precompute ATR reference for min gap filter
    def fvg_valid(gap_bounds: Tuple[float, float], bull: bool, bar_index_pos: int) -> bool:
        if variant.fvg_min_atr_frac <= 0:
            return True
        atr_val = atr_m5.iloc[bar_index_pos]
        if math.isnan(atr_val) or atr_val <= 0:
            return False
        if bull:
            size = gap_bounds[1] - gap_bounds[0]
        else:
            # bearish stored ordering ensures gap_bounds[0] is upper, [1] is lower
            size = gap_bounds[0] - gap_bounds[1]
        return size >= variant.fvg_min_atr_frac * atr_val

    # Long logic
    long_trade = None
    for i in range(len(after)):
        if i < 2 and variant.fvg_type == "fvg3":
            continue
        if i < 1 and variant.fvg_type == "fvg2":
            continue
        row = after.iloc[i]
        hi = float(row.high)
        prev_hi = float(after.iloc[i - 1].high) if i > 0 else hi
        bos_up = hi > or_high and prev_hi <= or_high
        if not bos_up:
            continue
        gap = detect_fvg(after, i, variant.fvg_type)
        if gap is None:
            continue
        # Determine bullish vs bearish gap nature
        bull_gap = gap[0] < gap[1]
        if not bull_gap:  # we need bullish for long
            continue
        if not fvg_valid(gap, True, after.index.get_loc(after.index[i])):
            continue
        # Demand candle = last red before BOS
        demand = None
        for j in range(i - 1, -1, -1):
            c = after.iloc[j]
            if c.close < c.open:
                demand = c
                demand_time = after.index[j]
                break
        if demand is None:
            continue
        zone_high = float(demand.high)
        zone_low = float(demand.low)
        breakout_time = after.index[i]
        breakout_extreme = hi
        entry_time = None
        entry_price = None
        if variant.entry_mode == "immediate":
            entry_time = breakout_time
            entry_price = float(row.close)
        else:  # retest
            forward = after.iloc[i + 1 :]
            for k in range(len(forward)):
                r2 = forward.iloc[k]
                if float(r2.low) <= zone_high:
                    entry_time = forward.index[k]
                    entry_price = zone_high
                    break
        if entry_price is None:
            break  # can't form this long; stop scanning further (first BOS basis)
        if variant.sl_mode == "or_extreme":
            sl = or_low - cfg.buffer_pips * cfg.pip_scale
        else:
            sl = zone_low - cfg.buffer_pips * cfg.pip_scale
        risk = entry_price - sl
        if risk <= 0:
            break
        if variant.tp_mode == "breakout":
            tp = breakout_extreme
        elif variant.tp_mode == "r_mult_2":
            tp = entry_price + 2 * risk
        else:  # r_mult_3
            tp = entry_price + 3 * risk
        long_trade = {
            "direction": "long",
            "entry_time": entry_time,
            "entry": entry_price,
            "sl": sl,
            "tp": tp,
            "or_high": or_high,
            "or_low": or_low,
            "breakout_time": breakout_time,
            "zone_high": zone_high,
            "zone_low": zone_low,
        }
        break

    # Short logic
    short_trade = None
    for i in range(len(after)):
        if i < 2 and variant.fvg_type == "fvg3":
            continue
        if i < 1 and variant.fvg_type == "fvg2":
            continue
        row = after.iloc[i]
        lo = float(row.low)
        prev_lo = float(after.iloc[i - 1].low) if i > 0 else lo
        bos_down = lo < or_low and prev_lo >= or_low
        if not bos_down:
            continue
        gap = detect_fvg(after, i, variant.fvg_type)
        if gap is None:
            continue
        bear_gap = gap[0] > gap[1]
        if not bear_gap:
            continue
        if not fvg_valid(gap, False, after.index.get_loc(after.index[i])):
            continue
        # Supply candle = last green before BOS
        supply = None
        for j in range(i - 1, -1, -1):
            c = after.iloc[j]
            if c.close > c.open:
                supply = c
                break
        if supply is None:
            continue
        zone_low = float(supply.low)
        zone_high = float(supply.high)
        breakout_time = after.index[i]
        breakout_extreme = lo
        entry_time = None
        entry_price = None
        if variant.entry_mode == "immediate":
            entry_time = breakout_time
            entry_price = float(row.close)
        else:
            forward = after.iloc[i + 1 :]
            for k in range(len(forward)):
                r2 = forward.iloc[k]
                if float(r2.high) >= zone_low:
                    entry_time = forward.index[k]
                    entry_price = zone_low
                    break
        if entry_price is None:
            break
        if variant.sl_mode == "or_extreme":
            sl = or_high + cfg.buffer_pips * cfg.pip_scale
        else:
            sl = zone_high + cfg.buffer_pips * cfg.pip_scale
        risk = sl - entry_price
        if risk <= 0:
            break
        if variant.tp_mode == "breakout":
            tp = breakout_extreme
        elif variant.tp_mode == "r_mult_2":
            tp = entry_price - 2 * risk
        else:
            tp = entry_price - 3 * risk
        short_trade = {
            "direction": "short",
            "entry_time": entry_time,
            "entry": entry_price,
            "sl": sl,
            "tp": tp,
            "or_high": or_high,
            "or_low": or_low,
            "breakout_time": breakout_time,
            "zone_high": zone_high,
            "zone_low": zone_low,
        }
        break

    # Simulate execution path: iterate bars after entry until SL or TP hit.
    def simulate(trade: Dict[str, Any]):
        direction = trade["direction"]
        entry_idx = m5.index.get_indexer([trade["entry_time"]])[0]
        following = m5.iloc[entry_idx + 1 : entry_idx + 600]  # limit horizon ~ 50h just in case
        exit_reason = None
        exit_price = None
        for ts, bar in following.iterrows():
            h = float(bar.high)
            l = float(bar.low)
            if direction == "long":
                # Check SL first (intra-bar)
                if l <= trade["sl"]:
                    exit_price = trade["sl"]
                    exit_reason = "SL"
                    break
                if h >= trade["tp"]:
                    exit_price = trade["tp"]
                    exit_reason = "TP"
                    break
            else:  # short
                if h >= trade["sl"]:
                    exit_price = trade["sl"]
                    exit_reason = "SL"
                    break
                if l <= trade["tp"]:
                    exit_price = trade["tp"]
                    exit_reason = "TP"
                    break
        if exit_price is None:
            # Force exit at last bar close (time stop) for neutrality
            ts = following.index[-1] if not following.empty else trade["entry_time"]
            exit_price = float(following.iloc[-1].close) if not following.empty else trade["entry"]
            exit_reason = "TIME" if not following.empty else "NO_BARS"
        trade["exit_time"] = ts
        trade["exit"] = exit_price
        trade["exit_reason"] = exit_reason
        # R calculation
        if direction == "long":
            r = (exit_price - trade["entry"]) / (trade["entry"] - trade["sl"])
        else:
            r = (trade["entry"] - exit_price) / (trade["sl"] - trade["entry"])
        trade["r_mult"] = r
        trade["hold_minutes"] = (trade["exit_time"] - trade["entry_time"]).total_seconds() / 60.0
        return trade

    for t in [long_trade, short_trade]:
        if t is not None:
            results.append(simulate(t))

    return results


# ----------------------------------------------------------------------------------
# Variant Matrix Construction
# ----------------------------------------------------------------------------------


def build_variants(expand: bool, entry_modes: Optional[List[str]] = None) -> List[Variant]:
    or_set = [15, 30, 60] if expand else [15, 30]
    entry_set = entry_modes if entry_modes else (["retest", "immediate"])
    fvg_types = ["fvg3", "fvg2"] if expand else ["fvg3"]
    fvg_min_fracs = [0.0, 0.25, 0.5] if expand else [0.0, 0.25]
    sl_modes = ["or_extreme", "zone"]
    tp_modes = ["breakout", "r_mult_2", "r_mult_3"] if expand else ["breakout", "r_mult_2"]

    variants = []
    for combo in itertools.product(or_set, entry_set, fvg_types, fvg_min_fracs, sl_modes, tp_modes):
        variants.append(Variant(*combo))
    return variants


# ----------------------------------------------------------------------------------
# Metrics Aggregation
# ----------------------------------------------------------------------------------


def aggregate_metrics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not trades:
        return {
            "trades": 0,
            "win_rate": 0.0,
            "avg_r": 0.0,
            "expectancy": 0.0,
            "pf": 0.0,
            "max_dd_r": 0.0,
            "med_hold_min": 0.0,
            "hit_tp_pct": 0.0,
        }
    rs = np.array([t["r_mult"] for t in trades])
    wins = rs[rs > 0]
    losses = rs[rs <= 0]
    win_rate = (rs > 0).mean()
    avg_win = wins.mean() if len(wins) else 0.0
    avg_loss = losses.mean() if len(losses) else 0.0
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_loss  # avg_loss negative already
    gross_win = wins.sum() if len(wins) else 0.0
    gross_loss = -losses.sum() if len(losses) else 0.0
    pf = gross_win / gross_loss if gross_loss > 0 else (gross_win if gross_win > 0 else 0.0)
    # Equity curve & max DD in R
    eq = np.cumsum(rs)
    peak = np.maximum.accumulate(eq)
    dd = eq - peak
    max_dd = dd.min() if len(dd) else 0.0
    med_hold = float(np.median([t["hold_minutes"] for t in trades])) if trades else 0.0
    hit_tp_pct = np.mean([t["exit_reason"] == "TP" for t in trades]) if trades else 0.0
    return {
        "trades": int(len(trades)),
        "win_rate": round(float(win_rate), 4),
        "avg_r": round(float(rs.mean()), 4),
        "expectancy": round(float(expectancy), 4),
        "pf": round(float(pf), 3),
        "max_dd_r": round(float(max_dd), 2),
        "med_hold_min": round(med_hold, 1),
        "hit_tp_pct": round(float(hit_tp_pct), 4),
    }


# ----------------------------------------------------------------------------------
# Main Runner
# ----------------------------------------------------------------------------------


def run_backtest(cfg: BacktestConfig, data_folder: str, entry_modes: Optional[List[str]], export: Optional[str]):
    symbol = cfg.symbol.upper()
    m5_path = os.path.join(data_folder, f"{symbol}_M5.csv")
    m15_path = os.path.join(data_folder, f"{symbol}_M15.csv")
    m5_df = load_csv_if_exists(m5_path)
    m15_df = load_csv_if_exists(m15_path)
    using_mock = False
    if m5_df is None or m15_df is None:
        print("[WARNING] Historical CSV not found or invalid. Generating MOCK data (results NOT tradable).")
        m5_df, m15_df = generate_mock_data(days=80)
        using_mock = True

    # Auto pip scale for JPY pairs
    if symbol.endswith("JPY"):
        cfg.pip_scale = 0.01

    # Filter by year if requested
    if cfg.year_filter:
        m5_df = m5_df[m5_df.index.year == cfg.year_filter]
        m15_df = m15_df[m15_df.index.year == cfg.year_filter]

    # Build per-day loop referencing local time zone midnight boundaries
    tz = cfg.tz_name
    # Convert index to local for day grouping quickly
    m5_local = m5_df.copy()
    m5_local["local_day"] = m5_local.index.tz_convert(tz).date
    unique_days = sorted(set(m5_local["local_day"]))
    if cfg.max_days:
        unique_days = unique_days[: cfg.max_days]

    atr_m5 = compute_atr(m5_df, period=14)
    variants = build_variants(cfg.expand_full_matrix, entry_modes)
    print(f"Running {len(variants)} variants over {len(unique_days)} days. Mock={using_mock}")

    all_variant_results: Dict[str, Dict[str, Any]] = {}
    variant_trade_store: Dict[str, List[Dict[str, Any]]] = {}

    for v in variants:
        trades: List[Dict[str, Any]] = []
        for d in unique_days:
            day_local_midnight = pd.Timestamp(d).tz_localize(tz)
            day_utc_start = day_local_midnight.tz_convert(timezone.utc)
            day_utc_end = day_utc_start + timedelta(days=1)
            day_m5 = m5_df[(m5_df.index >= day_utc_start) & (m5_df.index < day_utc_end)]
            day_m15 = m15_df[(m15_df.index >= day_utc_start) & (m15_df.index < day_utc_end)]
            if day_m5.empty or day_m15.empty:
                continue
            day_trades = evaluate_day(day_local_midnight, day_m5, day_m15, v, cfg, atr_m5)
            trades.extend(day_trades)
        metrics = aggregate_metrics(trades)
        all_variant_results[v.key()] = metrics
        variant_trade_store[v.key()] = trades

    df_results = pd.DataFrame.from_dict(all_variant_results, orient="index")
    df_results = df_results.sort_values(by=["expectancy", "pf"], ascending=[False, False])

    print("\nTop 10 Variants (sorted by Expectancy then PF):")
    print(df_results.head(10).to_string())

    if export:
        df_results.to_csv(export)
        print(f"Results exported -> {export}")

    # Return for programmatic use
    return df_results, variant_trade_store


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ORB FVG Variant Backtester")
    p.add_argument("--symbol", default="USDCAD")
    p.add_argument("--data-folder", default="data")
    p.add_argument("--year-filter", type=int, default=None)
    p.add_argument("--max-days", type=int, default=None)
    p.add_argument("--expand-full-matrix", action="store_true")
    p.add_argument("--entry-modes", nargs="*", default=None, help="Subset entry modes (retest immediate)")
    p.add_argument("--export", help="CSV path to export summary")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = BacktestConfig(
        symbol=args.symbol,
        year_filter=args.year_filter,
        max_days=args.max_days,
        expand_full_matrix=args.expand_full_matrix,
    )
    run_backtest(cfg, args.data_folder, args.entry_modes, args.export)


if __name__ == "__main__":
    main()
