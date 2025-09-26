from __future__ import annotations
"""
SMC MTF Analyzer & Signal Generator (standalone utility)

Changes vs user draft:
- data_dir now defaults to ./data relative to this file for easier local runs
- Added ensure_data() that can optionally synthesize small random-walk MT5 style CSVs when missing so script runs out-of-box
- Guarded main() to auto-create synthetic data if none found
"""
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Tuple
import os
import glob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

Timeframe = Literal["M1", "M5", "M15", "H1", "H4", "D1"]

# -------------------- Config --------------------


@dataclass
class Config:
    symbol: str = "USDCAD"
    correlated_symbol: Optional[str] = None  # e.g., "DXY"; if None, SMT checks are bypassed
    data_dir: str = os.path.join(os.path.dirname(__file__), "data")

    # Timeframes
    source_tfs: Tuple[Timeframe, Timeframe, Timeframe] = ("H4", "H1", "M15")
    confirm_tfs: Tuple[Timeframe, Timeframe, Timeframe] = ("M15", "M5", "M1")

    # Sweep detection
    sweep_lookback: int = 20  # bars for recent highs/lows

    # FVG / OB logic
    atr_period: int = 14
    displacement_atr_mult: float = 1.0  # min ATR multiple for a displacement (CoSD) candle
    max_pullback_candles: int = 5  # how many pullback candles to consider when forming OB from FVG

    # CoSD
    cosd_prior_break_bars: int = 2  # close above/below highs/lows of prior N bars

    # SMT
    smt_window: int = 50  # bars to find last two pivots
    smt_required: bool = False  # if True and correlated symbol missing, signals suppressed

    # Entry/TP/SL
    rr_tp_alt: float = 2.0  # 2R alternative TP
    entry_fill_window_bars: int = 24 * 60  # on M1: up to 1 day to get filled

    # NY session
    ny_tz: str = "America/New_York"
    ny_start: str = "10:00"
    ny_end: str = "17:00"
    data_tz: Optional[str] = None  # if None, treat index as naive

    # General swings
    swing_lookback: int = 3


# -------------------- IO & Utilities --------------------


def _read_mt5_csv(path: str) -> pd.DataFrame:
    # Fast path: standardized CSV (comma separated, 'date,time,open,...')
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        header = fh.readline().lower()
    if header.startswith('date,time,open,high,low,close'):
        df = pd.read_csv(path)
        if 'date' in df.columns and 'time' in df.columns:
            dt = pd.to_datetime(df['date'].astype(str)+' '+df['time'].astype(str), errors='coerce', format='%Y.%m.%d %H:%M:%S')
            df.index = dt
            pick_cols = [c for c in ["open","high","low","close","tickvol","vol","spread"] if c in df.columns]
            df = df[pick_cols].astype(float)
            df.sort_index(inplace=True)
            return df
    # Legacy TSV path
    df = pd.read_csv(path, sep="\t", engine="python")
    original_cols = set(df.columns)
    rename_map = {
        "<DATE>": "DATE",
        "<TIME>": "TIME",
        "<OPEN>": "open",
        "<HIGH>": "high",
        "<LOW>": "low",
        "<CLOSE>": "close",
        "<TICKVOL>": "tickvol",
        "<VOL>": "vol",
        "<SPREAD>": "spread",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    has_time = "<TIME>" in original_cols or "TIME" in df.columns
    if "TIME" not in df.columns:
        df["TIME"] = "00:00:00"
    if "DATE" not in df.columns or "TIME" not in df.columns:
        raise ValueError(f"CSV missing DATE/TIME columns after normalization: {path}")
    if not has_time:
        for col_tag, norm in [("<TICKVOL>", "tickvol"), ("<VOL>", "vol"), ("<SPREAD>", "spread")]:
            if norm not in df.columns and col_tag in df.columns:
                df[norm] = df[col_tag]
            if norm not in df.columns:
                df[norm] = 0
        agg = (
            df.groupby("DATE")
            .agg(
                open=("open", "first"),
                high=("high", "max"),
                low=("low", "min"),
                close=("close", "last"),
                tickvol=("tickvol", "sum"),
                vol=("vol", "sum"),
                spread=("spread", "last"),
            )
            .reset_index()
        )
        agg["TIME"] = "00:00:00"
        df = agg
    dt = pd.to_datetime(df["DATE"].astype(str) + " " + df["TIME"].astype(str), errors="coerce", format="%Y.%m.%d %H:%M:%S")
    bad = dt.isna()
    if bad.any():
        df = df.loc[~bad].copy()
        dt = dt.loc[~bad]
    df.index = dt
    needed = ["open", "high", "low", "close", "tickvol", "vol", "spread"]
    for col in needed:
        if col not in df.columns:
            orig = f"<{col.upper()}>"
            if orig in original_cols:
                df[col] = df[orig]
            else:
                df[col] = np.nan
    df = df[needed].astype(float)
    df.sort_index(inplace=True)
    return df


def _find_file(data_dir: str, symbol: str, tf: Timeframe) -> Optional[str]:
    std_patt = os.path.join(data_dir, f"{symbol}_{tf}_*-std.csv")
    matches = glob.glob(std_patt)
    if not matches:
        patt = os.path.join(data_dir, f"{symbol}_{tf}_*.csv")
        matches = glob.glob(patt)
    if not matches and tf == "D1":
        patt2 = os.path.join(data_dir, f"{symbol}_Daily_*.csv")
        matches = glob.glob(patt2)
    if not matches:
        return None
    return max(matches, key=lambda p: os.path.getsize(p))


def load_df_for(symbol: str, tf: Timeframe, cfg: Config) -> Optional[pd.DataFrame]:
    fp = _find_file(cfg.data_dir, symbol, tf)
    if not fp:
        return None
    return _read_mt5_csv(fp)


def load_multi(cfg: Config, symbol: str, tfs: List[Timeframe]) -> Dict[Timeframe, pd.DataFrame]:
    out: Dict[Timeframe, pd.DataFrame] = {}
    for tf in tfs:
        df = load_df_for(symbol, tf, cfg)
        if df is not None:
            out[tf] = df
    return out


def to_ny_flags(df: pd.DataFrame, cfg: Config) -> Tuple[pd.Series, pd.Series]:
    idx = df.index
    if cfg.data_tz:
        if idx.tz is None:
            idx_ny = idx.tz_localize(cfg.data_tz).tz_convert(cfg.ny_tz)
        else:
            idx_ny = idx.tz_convert(cfg.ny_tz)
    else:
        idx_ny = idx.tz_localize("UTC").tz_convert(cfg.ny_tz)
    start_h, start_m = map(int, cfg.ny_start.split(":"))
    end_h, end_m = map(int, cfg.ny_end.split(":"))
    local_times = idx_ny.tz_localize(None)
    hours = pd.Series(local_times.hour, index=df.index)
    minutes = pd.Series(local_times.minute, index=df.index)
    in_sess = ((hours > start_h) | ((hours == start_h) & (minutes >= start_m))) & (
        (hours < end_h) | ((hours == end_h) & (minutes <= end_m))
    )
    in_sess = in_sess.astype(bool)
    start_flag = in_sess & (~in_sess.shift(1).fillna(False))
    return in_sess, start_flag


def daily_bias(d1: pd.DataFrame) -> pd.Series:
    prev_close = d1["close"].shift(1)
    prev_high = d1["high"].shift(1)
    prev_low = d1["low"].shift(1)
    bias = pd.Series(0, index=d1.index, dtype=int)
    bias[(prev_close > prev_high)] = +1
    bias[(prev_close < prev_low)] = -1
    return bias

# -------------------- Core detections --------------------

def swing_pivots(df: pd.DataFrame, lookback: int) -> Tuple[pd.Series, pd.Series]:
    high = df["high"].values
    low = df["low"].values
    n = len(df)
    piv_h = np.zeros(n, dtype=bool)
    piv_l = np.zeros(n, dtype=bool)
    for i in range(lookback, n - lookback):
        if high[i] == np.max(high[i - lookback : i + lookback + 1]):
            piv_h[i] = True
        if low[i] == np.min(low[i - lookback : i + lookback + 1]):
            piv_l[i] = True
    return pd.Series(piv_h, index=df.index), pd.Series(piv_l, index=df.index)

def detect_sweeps(df: pd.DataFrame, lookback: int) -> pd.DataFrame:
    highs = df["high"].rolling(lookback, min_periods=lookback).max().shift(1)
    lows = df["low"].rolling(lookback, min_periods=lookback).min().shift(1)
    sh = (df["high"] > highs) & (df["close"] <= highs)
    sl = (df["low"] < lows) & (df["close"] >= lows)
    return pd.DataFrame({"sweep_high": sh.fillna(False), "sweep_low": sl.fillna(False)}, index=df.index)

def detect_fvg(df: pd.DataFrame) -> List[Tuple[pd.Timestamp, float, float, Literal["bull", "bear"]]]:
    lows = df["low"].values
    highs = df["high"].values
    idx = df.index
    out: List[Tuple[pd.Timestamp, float, float, Literal["bull", "bear"]]] = []
    for i in range(3, len(df)):
        t_right = idx[i - 1]
        if highs[i - 3] < lows[i - 1]:
            out.append((t_right, float(lows[i - 1]), float(highs[i - 3]), "bull"))
        elif lows[i - 3] > highs[i - 1]:
            out.append((t_right, float(lows[i - 3]), float(highs[i - 1]), "bear"))
    return out

@dataclass
class Zone:
    kind: Literal["FVG", "OB", "BB"]
    tf: Timeframe
    start_time: pd.Timestamp
    end_time: pd.Timestamp
    low: float
    high: float
    direction: Literal["bull", "bear"]
    @property
    def mid(self) -> float:
        return (self.low + self.high) / 2.0

def build_ob_from_fvg(df: pd.DataFrame, tf: Timeframe, max_pullback_candles: int) -> List[Zone]:
    fvgs = detect_fvg(df)
    zones: List[Zone] = []
    o = df["open"]; c = df["close"]; h = df["high"]; l = df["low"]; idx = df.index
    for t_right, top, bottom, direction in fvgs:
        i_right = df.index.get_loc(t_right)
        j_end = min(len(df) - 1, i_right + 1 + max_pullback_candles)
        starter_idx: Optional[int] = None
        if direction == "bull":
            for j in range(i_right + 1, j_end + 1):
                if c.iloc[j] < o.iloc[j] and l.iloc[j] <= top and h.iloc[j] >= bottom:
                    starter_idx = j; break
            if starter_idx is None: continue
            body_low = min(o.iloc[starter_idx], c.iloc[starter_idx])
            body_high = max(o.iloc[starter_idx], c.iloc[starter_idx])
            confirmed_idx = None
            for k in range(starter_idx + 1, min(starter_idx + 20, len(df))):
                if c.iloc[k] > body_high: confirmed_idx = k; break
            if confirmed_idx is None: continue
            zones.append(Zone(kind="OB", tf=tf, start_time=idx[starter_idx], end_time=idx[confirmed_idx], low=float(body_low), high=float(body_high), direction="bull"))
        else:
            for j in range(i_right + 1, j_end + 1):
                if c.iloc[j] > o.iloc[j] and l.iloc[j] <= top and h.iloc[j] >= bottom:
                    starter_idx = j; break
            if starter_idx is None: continue
            body_low = min(o.iloc[starter_idx], c.iloc[starter_idx])
            body_high = max(o.iloc[starter_idx], c.iloc[starter_idx])
            confirmed_idx = None
            for k in range(starter_idx + 1, min(starter_idx + 20, len(df))):
                if c.iloc[k] < body_low: confirmed_idx = k; break
            if confirmed_idx is None: continue
            zones.append(Zone(kind="OB", tf=tf, start_time=idx[starter_idx], end_time=idx[confirmed_idx], low=float(body_low), high=float(body_high), direction="bear"))
    return zones

def build_fvg_zones(df: pd.DataFrame, tf: Timeframe) -> List[Zone]:
    out: List[Zone] = []
    for t_right, top, bottom, direction in detect_fvg(df):
        lo, hi = (min(top, bottom), max(top, bottom))
        out.append(Zone(kind="FVG", tf=tf, start_time=t_right, end_time=t_right, low=lo, high=hi, direction=direction))
    return out

def atr(df: pd.DataFrame, period: int) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"].shift(1)
    tr = pd.concat([(h - l), (h - c).abs(), (l - c).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()

def displacement_cosd(df: pd.DataFrame, start_time: pd.Timestamp, prior_break_bars: int, atr_mult: float, atr_period: int) -> Optional[Tuple[pd.Timestamp, Literal["bull", "bear"], float, float]]:
    sub = df.loc[start_time:]
    if sub.empty: return None
    a = atr(sub, atr_period)
    idx = sub.index
    for i in range(prior_break_bars, len(sub)):
        t = idx[i]; row = sub.iloc[i]; rng = float(row["high"] - row["low"])
        if not np.isfinite(a.iloc[i]) or rng < atr_mult * a.iloc[i]: continue
        prior_hi = float(sub["high"].iloc[i - prior_break_bars : i].max())
        prior_lo = float(sub["low"].iloc[i - prior_break_bars : i].min())
        if float(row["close"]) > prior_hi:
            return t, "bull", float(row["low"]), float(row["high"])
        if float(row["close"]) < prior_lo:
            return t, "bear", float(row["low"]), float(row["high"])
    return None

def unmitigated(z: Zone, df: pd.DataFrame, up_to: pd.Timestamp) -> bool:
    w = df.loc[z.end_time:up_to]
    if w.empty: return True
    if z.direction == "bull":
        touched = (w["low"] <= z.high).any()
    else:
        touched = (w["high"] >= z.low).any()
    return not touched

def first_touch_now(z: Zone, row: pd.Series, df: pd.DataFrame) -> bool:
    t = row.name
    prior = df.loc[z.end_time:t].iloc[:-1]
    if z.direction == "bull":
        prior_touched = (prior["low"] <= z.high).any() if not prior.empty else False
        now_touch = row["low"] <= z.high
    else:
        prior_touched = (prior["high"] >= z.low).any() if not prior.empty else False
        now_touch = row["high"] >= z.low
    return now_touch and not prior_touched

# -------------------- SMT Divergence --------------------

def smt_divergence(main: pd.DataFrame, corr: pd.DataFrame, t: pd.Timestamp, window: int, lookback: int) -> Optional[Literal["bull", "bear"]]:
    msub = main.loc[:t].tail(window)
    csub = corr.loc[:t].tail(window)
    if len(msub) < window // 2 or len(csub) < window // 2: return None
    msh, msl = swing_pivots(msub, lookback); csh, csl = swing_pivots(csub, lookback)
    m_hi = msub[msh]["high"].tail(2); m_lo = msub[msl]["low"].tail(2)
    c_hi = csub[csh]["high"].tail(2); c_lo = csub[csl]["low"].tail(2)
    sig: Optional[Literal["bull", "bear"]] = None
    if len(m_lo) == 2 and len(c_lo) == 2:
        m_ll = float(m_lo.iloc[-1]) < float(m_lo.iloc[0])
        c_ll = float(c_lo.iloc[-1]) < float(c_lo.iloc[0])
        if m_ll and (not c_ll): sig = "bull"
    if len(m_hi) == 2 and len(c_hi) == 2:
        m_hh = float(m_hi.iloc[-1]) > float(m_hi.iloc[0])
        c_hh = float(c_hi.iloc[-1]) > float(c_hi.iloc[0])
        if m_hh and (not c_hh): sig = "bear"
    return sig

# -------------------- Signal engine --------------------

@dataclass
class Signal:
    time: pd.Timestamp
    src_tf: Timeframe
    confirm_tf: Timeframe
    direction: Literal["long", "short"]
    reason: str
    entry: float
    sl: float
    tp: float
    ny_session: bool
    daily_bias: int
    pd_kind: Literal["FVG", "OB", "BB"]
    pd_low: float
    pd_high: float

def opposing_liquidity_tp(df: pd.DataFrame, t: pd.Timestamp, direction: Literal["long", "short"], lookback: int) -> Optional[float]:
    sub = df.loc[t:]
    if sub.empty: return None
    sh, sl = swing_pivots(sub, lookback)
    if direction == "long":
        highs = sub[sh]["high"]
        return float(highs.iloc[0]) if not highs.empty else None
    else:
        lows = sub[sl]["low"]
        return float(lows.iloc[0]) if not lows.empty else None

def generate_signals(cfg: Config) -> pd.DataFrame:
    need_tfs = ["D1", "H4", "H1", "M15", "M5", "M1"]
    dfs = load_multi(cfg, cfg.symbol, need_tfs)
    missing = [tf for tf in need_tfs if tf not in dfs]
    if any(tf in ("D1", "H4", "H1", "M15", "M1") for tf in missing):
        raise RuntimeError(f"Missing required timeframes for {cfg.symbol}: {missing}")
    corr_dfs: Dict[Timeframe, pd.DataFrame] = {}
    if cfg.correlated_symbol:
        corr_dfs = load_multi(cfg, cfg.correlated_symbol, ["H4", "H1", "M15", "M5", "M1"])
        if cfg.smt_required and not corr_dfs:
            raise RuntimeError("SMT required but correlated asset data not found")
    d1 = dfs["D1"]; bias_series = daily_bias(d1)
    m1 = dfs["M1"]; m5 = dfs.get("M5"); m15 = dfs["M15"]; h1 = dfs["H1"]; h4 = dfs["H4"]
    ny_in, ny_start = to_ny_flags(m1, cfg)
    src_map: Dict[Timeframe, pd.DataFrame] = {"H4": h4, "H1": h1, "M15": m15}
    pd_zones: Dict[Timeframe, List[Zone]] = {tf: [] for tf in cfg.source_tfs}
    for tf in cfg.source_tfs:
        df = src_map[tf]
        pd_zones[tf].extend(build_fvg_zones(df, tf))
        pd_zones[tf].extend(build_ob_from_fvg(df, tf, cfg.max_pullback_candles))
    sweeps: Dict[Timeframe, pd.DataFrame] = {tf: detect_sweeps(src_map[tf], cfg.sweep_lookback) for tf in cfg.source_tfs}
    confirm_for: Dict[Timeframe, Timeframe] = {cfg.source_tfs[0]: cfg.confirm_tfs[0], cfg.source_tfs[1]: cfg.confirm_tfs[1], cfg.source_tfs[2]: cfg.confirm_tfs[2]}
    conf_map: Dict[Timeframe, pd.DataFrame] = {"M15": m15, "M5": m5 if m5 is not None else m15, "M1": m1}
    signals: List[Signal] = []
    for src_tf in cfg.source_tfs:
        src_df = src_map[src_tf]; conf_tf = confirm_for[src_tf]; conf_df = conf_map[conf_tf]
        sw = sweeps[src_tf]
        for t in src_df.index:
            srow = src_df.loc[t]
            sh = bool(sw.loc[t, "sweep_high"]) if t in sw.index else False
            slw = bool(sw.loc[t, "sweep_low"]) if t in sw.index else False
            if not (sh or slw): continue
            candidates = [z for z in pd_zones[src_tf] if z.end_time <= t]
            touched_now = [z for z in candidates if first_touch_now(z, srow, src_df)]
            if not touched_now: continue
            want_dir: Literal["long", "short"] = "short" if sh else "long"
            touched_now = [z for z in touched_now if (z.direction == ("bear" if want_dir == "short" else "bull"))]
            if not touched_now: continue
            cosd = displacement_cosd(conf_df, t, cfg.cosd_prior_break_bars, cfg.displacement_atr_mult, cfg.atr_period)
            if cosd is None: continue
            cosd_time, cosd_dir, cosd_low, cosd_high = cosd
            if (want_dir == "long" and cosd_dir != "bull") or (want_dir == "short" and cosd_dir != "bear"): continue
            if cfg.correlated_symbol and conf_tf in corr_dfs:
                corr_df = corr_dfs.get(conf_tf)
                if corr_df is not None:
                    smt_sig = smt_divergence(conf_df, corr_df, cosd_time, cfg.smt_window, cfg.swing_lookback)
                    if cfg.smt_required and smt_sig is None: continue
                    if smt_sig is not None:
                        if (want_dir == "long" and smt_sig != "bull") or (want_dir == "short" and smt_sig != "bear"): continue
            entry = (cosd_low + cosd_high) / 2.0
            if want_dir == "long":
                sl = float(cosd_low); risk = max(entry - sl, 1e-6)
            else:
                sl = float(cosd_high); risk = max(sl - entry, 1e-6)
            opp = opposing_liquidity_tp(conf_df, cosd_time, want_dir, cfg.swing_lookback)
            tp_rr = entry + cfg.rr_tp_alt * risk if want_dir == "long" else entry - cfg.rr_tp_alt * risk
            if opp is not None:
                tp = min(tp_rr, opp) if want_dir == "long" else max(tp_rr, opp)
            else:
                tp = tp_rr
            m1_pos = m1.index.searchsorted(cosd_time, side="right") - 1
            m1_pos = max(0, min(m1_pos, len(m1.index) - 1))
            m1_time = m1.index[m1_pos]
            ny_flag = bool(ny_in.loc[m1_time])
            d_key = pd.Timestamp(year=m1_time.year, month=m1_time.month, day=m1_time.day)
            b_sub = bias_series.loc[:d_key]
            d_bias = int(b_sub.iloc[-1]) if not b_sub.empty else 0
            z_used = None
            for z in touched_now:
                if z.kind == "OB": z_used = z; break
            if z_used is None: z_used = touched_now[0]
            signals.append(Signal(time=cosd_time, src_tf=src_tf, confirm_tf=conf_tf, direction=want_dir, reason=("sweep + PD touch + CoSD"), entry=float(entry), sl=float(sl), tp=float(tp), ny_session=ny_flag, daily_bias=d_bias, pd_kind=z_used.kind, pd_low=float(z_used.low), pd_high=float(z_used.high)))
    if not signals:
        return pd.DataFrame(columns=["time", "src_tf", "confirm_tf", "direction", "reason", "entry", "sl", "tp", "ny_session", "daily_bias", "pd_kind", "pd_low", "pd_high"])
    df = pd.DataFrame([s.__dict__ for s in signals]); df.sort_values("time", inplace=True); return df

# ------------- Synthetic data helper -------------

_TF_MINUTES = {"M1":1,"M5":5,"M15":15,"H1":60,"H4":240,"D1":1440}

def _synth_tf_series(start: datetime, bars: int, tf: Timeframe, base: float) -> pd.DataFrame:
    freq_min = _TF_MINUTES[tf]
    idx = [start + timedelta(minutes=freq_min*i) for i in range(bars)]
    prices = base + np.cumsum(np.random.normal(0, 0.05, size=bars))
    spread = 1
    o = prices + np.random.normal(0, 0.01, size=bars)
    h = o + np.abs(np.random.normal(0.05, 0.02, size=bars))
    l = o - np.abs(np.random.normal(0.05, 0.02, size=bars))
    c = l + (h-l)*np.random.rand(bars)
    df = pd.DataFrame({"open":o,"high":h,"low":l,"close":c,"tickvol":100,"vol":0,"spread":spread}, index=pd.to_datetime(idx))
    return df

def ensure_data(cfg: Config, min_bars: Dict[Timeframe,int]|None=None):
    os.makedirs(cfg.data_dir, exist_ok=True)
    if min_bars is None:
        min_bars = {"D1":120,"H4":400,"H1":800,"M15":2000,"M5":4000,"M1":8000}
    existing = load_multi(cfg, cfg.symbol, list(min_bars.keys()))
    for tf, req in min_bars.items():
        if tf in existing and len(existing[tf]) >= req//2:  # accept half length
            continue
        # synthesize
        bars = req
        start = datetime.utcnow() - timedelta(minutes=_TF_MINUTES[tf]*bars)
        base = 1.30
        df = _synth_tf_series(start, bars, tf, base)
        # write standardized csv format
        out_name = f"{cfg.symbol}_{tf}_synthetic-std.csv"
        path = os.path.join(cfg.data_dir, out_name)
        df_reset = df.reset_index()
        df_reset["date"] = df_reset["index"].dt.strftime("%Y.%m.%d")
        df_reset["time"] = df_reset["index"].dt.strftime("%H:%M:%S")
        cols = ["date","time","open","high","low","close","tickvol","vol","spread"]
        df_reset[cols].to_csv(path, index=False)

# -------------------- Main --------------------

def main():
    cfg = Config()
    ensure_data(cfg)  # create synthetic if missing
    try:
        sigs = generate_signals(cfg)
    except RuntimeError as e:
        print(f"Error generating signals: {e}")
        return
    out = os.path.join(os.path.dirname(__file__), f"smc-mtf-signals-{cfg.symbol}.csv")
    sigs.to_csv(out, index=False)
    print(f"Generated {len(sigs)} signals -> {out}")

if __name__ == "__main__":
    main()
