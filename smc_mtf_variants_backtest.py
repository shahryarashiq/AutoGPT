"""
SMC MTF Strategy Variant Backtester & Parameter Sweeper
=======================================================

This script builds on `smc_mtf.py` (signal generation) and adds / fixes:

1. Signal backtesting (fills, SL/TP logic, equity curve)
2. Rich performance metrics (R stats, profit factor, drawdown, Sharpe, etc.)
3. Parameter grid search (sweeps core config variables)
4. Output artifacts:
   - variants_summary.csv (one row per parameter combination)
   - best_variant_trades.csv (detailed trade log of best performing variant)
   - equity_curve_best.csv (timestamped equity curve of best variant)
   - backtests/variant_<N>_trades.csv (all variants if `save_all_trade_logs=True`)
5. Enhanced metrics: CAGR, MAR ratio, risk of ruin estimate, R distribution stats
6. Safer fill logic & optional compounding

Assumptions / Simplifications
-----------------------------
* Synthetic data (if real data absent) means absolute P/L is not meaningful; focus on relative metrics.
* FX pip value model: pip_size=0.0001, contract_size=100_000, pip_value_per_standard_lot=10 quote units.
* Fixed lot size (0.01) per user request. Risk per trade therefore variable in % terms.
* If a bar touches both SL & TP we assume SL hit first (conservative) unless `assume_tp_first=True`.
* Fills occur when the intrabar high/low envelope includes the entry price AFTER signal time, within a max number of minutes specified by config.entry_fill_window_bars (interpreted on M1 timeline).
* R (reward-risk) uses initial (entry-SL) absolute distance; partial exits not modeled.

Key Metrics Reported
--------------------
* trades / wins / losses / win_rate
* longs / shorts distribution
* tp_hits / sl_hits
* avg_R, median_R, expectancy_R (avg win * win_rate - avg loss * loss_rate)
* profit_factor (gross_profit / gross_loss_abs)
* net_profit, return_pct (vs starting balance)
* max_drawdown_abs / max_drawdown_pct
* sharpe_R (per trade R Sharpe, sqrt(n) scaled)
* avg_hold_bars / median_hold_bars
* ny_session_win_rate
* zone kind distribution (OB/FVG/BB) and bias alignment win rate

Usage
-----
Run directly:
  python smc_mtf_variants_backtest.py

Adjust parameter grid or runtime settings in `PARAM_GRID` and `RuntimeSettings` below.

NOTE: For large grids the runtime grows quickly. Use `max_variants` to cap combinations.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, List, Optional, Tuple
import itertools
import math
import os
import random
import time
import statistics as stats
try:  # optional advanced stats
    from scipy.stats import skew as _scipy_skew, kurtosis as _scipy_kurtosis
except Exception:  # pragma: no cover
    _scipy_skew = None
    _scipy_kurtosis = None

import numpy as np
import pandas as pd
try:
    import matplotlib.pyplot as plt  # optional for equity curve
except Exception:  # pragma: no cover - plotting optional
    plt = None

from smc_mtf import (
    Config,
    ensure_data,
    generate_signals,
    load_df_for,
    Timeframe,
    _TF_MINUTES,
)


# ---------------- Runtime / Grid Config ----------------

PARAM_GRID: Dict[str, List[Any]] = {
    # Keep sizes modest first; expand later once stable (user can enlarge)
    "displacement_atr_mult": [0.8, 1.0, 1.2],
    "sweep_lookback": [15, 20, 30],
    "cosd_prior_break_bars": [1, 2],
    "rr_tp_alt": [1.5, 2.0, 2.5],
    "max_pullback_candles": [3, 5, 7],
}


@dataclass
class RuntimeSettings:
    start_balance: float = 500.0
    lot_size: float = 0.01  # fixed lot
    pip_size: float = 0.0001
    contract_size: int = 100_000  # standard FX
    assume_tp_first: bool = False
    min_trades_for_viable: int = 15
    max_variants: int = 120  # cap total combos (randomly sampled if exceeded)
    random_seed: int = 42
    save_all_trade_logs: bool = False
    out_dir: str = os.path.join(os.path.dirname(__file__), "backtests")
    compound: bool = False  # if True risk model could scale; placeholder for future sizing
    save_equity_plot: bool = False
    equity_plot_filename: str = "equity_curve_best.png"


RUNTIME = RuntimeSettings()


# ---------------- Backtest Core ----------------

def _pip_value(lot_size: float, contract_size: int, pip_size: float) -> float:
    return (contract_size * pip_size) * lot_size  # e.g., 10 * lot_size for majors


def _find_fill(m1: pd.DataFrame, start_time: pd.Timestamp, entry: float, direction: str, fill_window_bars: int) -> Optional[pd.Timestamp]:
    """Return first timestamp within window where price range envelops entry.

    Uses position-based slicing for speed & to avoid potential timezone / duplicate index issues.
    """
    if start_time not in m1.index:
        # find insertion point (signal may be between M1 bars)
        pos = m1.index.searchsorted(start_time, side="left")
    else:
        pos = m1.index.get_loc(start_time)
    end = min(len(m1.index), pos + fill_window_bars)
    for i in range(pos, end):
        row = m1.iloc[i]
        lo = float(row["low"]); hi = float(row["high"])
        if lo <= entry <= hi:
            return m1.index[i]
    return None


def _bar_hit(row: pd.Series, price: float, direction: str, sl: float, tp: float, assume_tp_first: bool) -> Optional[str]:
    lo = float(row["low"]); hi = float(row["high"])
    if direction == "long":
        hit_sl = lo <= sl
        hit_tp = hi >= tp
        if hit_sl and hit_tp:
            return "tp" if assume_tp_first else "sl"
        if hit_tp:
            return "tp"
        if hit_sl:
            return "sl"
    else:  # short
        hit_sl = hi >= sl
        hit_tp = lo <= tp
        if hit_sl and hit_tp:
            return "tp" if assume_tp_first else "sl"
        if hit_tp:
            return "tp"
        if hit_sl:
            return "sl"
    return None


def backtest_signals(
    signals: pd.DataFrame,
    m1: pd.DataFrame,
    cfg: Config,
    rt: RuntimeSettings,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    if signals.empty:
        return (
            pd.DataFrame(columns=[
                "signal_time","fill_time","exit_time","direction","entry","sl","tp","exit_price","result","R","pips","profit","hold_bars","pd_kind","daily_bias","ny_session"
            ]),
            pd.DataFrame(columns=["time","equity"]),
            {"trades":0}
        )

    pip_value = _pip_value(rt.lot_size, rt.contract_size, rt.pip_size)
    balance = rt.start_balance
    equity_curve = []  # (time, equity)
    trade_rows = []
    last_time = None

    for _, sig in signals.iterrows():
        sig_time = pd.to_datetime(sig["time"])
        entry = float(sig["entry"])
        sl = float(sig["sl"])
        tp = float(sig["tp"])
        direction = sig["direction"]

        fill_t = _find_fill(m1, sig_time, entry, direction, cfg.entry_fill_window_bars)
        if fill_t is None:
            continue
        sub = m1.loc[fill_t:]
        exit_price = None
        exit_time = None
        result = None
        risk = (entry - sl) if direction == "long" else (sl - entry)
        risk = abs(risk)
        for t, row in sub.iloc[1:].iterrows():  # start after fill bar
            which = _bar_hit(row, entry, direction, sl, tp, rt.assume_tp_first)
            if which:
                exit_time = t
                if which == "tp":
                    exit_price = tp
                    result = "tp"
                else:
                    exit_price = sl
                    result = "sl"
                break
        if exit_time is None:
            # force exit at last available bar (flat) if unmoved
            exit_time = sub.index[-1]
            # flat at close
            exit_price = float(sub.iloc[-1]["close"])
            result = "timeout"

        # Compute R / pips
        if direction == "long":
            pnl_price = exit_price - entry
            r_mult = pnl_price / risk if risk > 0 else 0.0
        else:
            pnl_price = entry - exit_price
            r_mult = pnl_price / risk if risk > 0 else 0.0
        pips = pnl_price / rt.pip_size
        profit = pips * pip_value  # simplified FX P/L (no commissions modeled)
        # Placeholder for compounding position sizing logic if enabled later
        balance += profit
        hold_bars = m1.index.get_indexer([exit_time])[0] - m1.index.get_indexer([fill_t])[0]
        trade_rows.append({
            "signal_time": sig_time,
            "fill_time": fill_t,
            "exit_time": exit_time,
            "direction": direction,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "exit_price": exit_price,
            "result": result,
            "R": r_mult,
            "pips": pips,
            "profit": profit,
            "balance_after": balance,
            "hold_bars": hold_bars,
            "pd_kind": sig["pd_kind"],
            "daily_bias": sig["daily_bias"],
            "ny_session": sig["ny_session"],
        })
        equity_curve.append((exit_time, balance))
        last_time = exit_time

    trades_df = pd.DataFrame(trade_rows)
    if trades_df.empty:
        return trades_df, pd.DataFrame(columns=["time","equity"]), {"trades":0}

    eq_df = pd.DataFrame(equity_curve, columns=["time","equity"]).sort_values("time")

    metrics = compute_metrics(trades_df, eq_df, rt)
    return trades_df, eq_df, metrics


def compute_metrics(trades: pd.DataFrame, equity: pd.DataFrame, rt: RuntimeSettings) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    n = len(trades)
    out["trades"] = n
    wins = trades[trades["R"] > 0]
    losses = trades[trades["R"] < 0]
    tp_hits = trades[trades["result"] == "tp"]
    sl_hits = trades[trades["result"] == "sl"]
    out["wins"] = len(wins)
    out["losses"] = len(losses)
    out["win_rate"] = len(wins) / n if n else 0.0
    out["tp_hits"] = len(tp_hits)
    out["sl_hits"] = len(sl_hits)
    longs = trades[trades["direction"] == "long"]
    shorts = trades[trades["direction"] == "short"]
    out["long_trades"] = len(longs)
    out["short_trades"] = len(shorts)
    out["avg_R"] = trades["R"].mean() if n else 0.0
    out["median_R"] = trades["R"].median() if n else 0.0
    avg_win_R = wins["R"].mean() if len(wins) else 0.0
    avg_loss_R = abs(losses["R"].mean()) if len(losses) else 0.0
    out["avg_win_R"] = avg_win_R
    out["avg_loss_R"] = avg_loss_R
    out["expectancy_R"] = out["win_rate"] * avg_win_R - (1 - out["win_rate"]) * avg_loss_R
    gross_profit = wins["profit"].sum()
    gross_loss = losses["profit"].sum()  # negative
    out["profit_factor"] = (gross_profit / abs(gross_loss)) if gross_loss < 0 else np.nan
    out["net_profit"] = trades["profit"].sum()
    out["return_pct"] = (equity["equity"].iloc[-1] / rt.start_balance - 1) * 100 if not equity.empty else 0
    # Drawdown
    if not equity.empty:
        peak = equity["equity"].cummax()
        dd = (equity["equity"] - peak)
        max_dd = dd.min()
        out["max_drawdown_abs"] = max_dd
        out["max_drawdown_pct"] = (max_dd / peak.max()) * 100 if peak.max() else 0
        # Store additional risk stats
        out["avg_drawdown_abs"] = dd.mean()
        out["equity_final"] = float(equity["equity"].iloc[-1])
    else:
        out["max_drawdown_abs"] = 0
        out["max_drawdown_pct"] = 0
        out["avg_drawdown_abs"] = 0
        out["equity_final"] = rt.start_balance
    # Sharpe (per trade R)
    if n > 1:
        r_series = trades["R"].values
        r_mean = r_series.mean()
        r_std = r_series.std(ddof=1)
        out["sharpe_R"] = (r_mean / r_std) * math.sqrt(n) if r_std > 1e-9 else np.nan
    else:
        out["sharpe_R"] = np.nan
    out["avg_hold_bars"] = trades["hold_bars"].mean() if n else 0
    out["median_hold_bars"] = trades["hold_bars"].median() if n else 0
    # R distribution & expectancy quality
    if n:
        r_vals = trades["R"].values
        out["R_std"] = float(np.std(r_vals, ddof=1)) if n > 1 else 0.0
        if _scipy_skew is not None and n > 2:
            out["R_skew"] = float(_scipy_skew(r_vals, bias=False))
        else:
            out["R_skew"] = 0.0
        if _scipy_kurtosis is not None and n > 3:
            out["R_kurtosis"] = float(_scipy_kurtosis(r_vals, bias=False, fisher=True))
        else:
            out["R_kurtosis"] = 0.0
        out["R_95pct"] = float(np.percentile(r_vals, 95))
        out["R_05pct"] = float(np.percentile(r_vals, 5))
    else:
        out.update({"R_std":0.0,"R_skew":0.0,"R_kurtosis":0.0,"R_95pct":0.0,"R_05pct":0.0})
    # CAGR & MAR (assumes equity period length approximated by trade spacing)
    if n > 1:
        start_t = trades["fill_time"].iloc[0]; end_t = trades["exit_time"].iloc[-1]
        days = max(1, (end_t - start_t).days)
        years = days / 365.25
        if years > 0:
            cagr = (out["equity_final"] / rt.start_balance) ** (1 / years) - 1
            out["CAGR"] = cagr
            max_dd_pct = abs(out.get("max_drawdown_pct", 0)) / 100
            out["MAR"] = cagr / max_dd_pct if max_dd_pct > 0 else np.nan
        else:
            out["CAGR"] = np.nan; out["MAR"] = np.nan
    else:
        out["CAGR"] = np.nan; out["MAR"] = np.nan
    # Profit per trade & risk of ruin (approx)
    out["profit_per_trade"] = out["net_profit"] / n if n else 0
    # Risk of ruin simplistic model using R stats
    if n and avg_win_R > 0 and avg_loss_R > 0:
        p = out["win_rate"]; q = 1 - p
        b = avg_win_R / avg_loss_R  # payoff ratio
        edge = p * b - q
        if edge <= 0:
            out["risk_of_ruin"] = 1.0
        else:
            # Using simplified formula: RoR = ((q/b)/p)**capital_units (capital units ~ net R cushion)
            net_R = trades["R"].sum()
            capital_units = max(1, net_R / avg_loss_R)  # rough cushion in loss units
            ror = ((q / b) / p) ** capital_units if p > 0 else 1.0
            out["risk_of_ruin"] = min(1.0, max(0.0, ror))
    else:
        out["risk_of_ruin"] = np.nan
    ny = trades[trades["ny_session"] == True]
    if not ny.empty:
        ny_w = ny[ny["R"] > 0]
        out["ny_session_win_rate"] = len(ny_w) / len(ny)
    else:
        out["ny_session_win_rate"] = np.nan
    # Zone kind distribution win rates
    for kind in trades["pd_kind"].unique():
        subset = trades[trades["pd_kind"] == kind]
        if subset.empty:
            continue
        out[f"zone_{kind}_trades"] = len(subset)
        out[f"zone_{kind}_win_rate"] = (subset[subset["R"] > 0].shape[0] / len(subset))
    # Bias alignment win rate (when daily_bias aligns with direction) simplistic
    align_mask = (
        ((trades["daily_bias"] > 0) & (trades["direction"] == "long"))
        | ((trades["daily_bias"] < 0) & (trades["direction"] == "short"))
    )
    aligned = trades[align_mask]
    if not aligned.empty:
        out["bias_aligned_win_rate"] = (aligned[aligned["R"] > 0].shape[0] / len(aligned))
    else:
        out["bias_aligned_win_rate"] = np.nan
    return out


# ---------------- Parameter Sweep ----------------

def parameter_combinations(grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    keys = list(grid.keys())
    value_lists = [grid[k] for k in keys]
    combos = []
    for values in itertools.product(*value_lists):
        combos.append({k: v for k, v in zip(keys, values)})
    return combos


def run_parameter_grid(base_cfg: Config, rt: RuntimeSettings) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    combos = parameter_combinations(PARAM_GRID)
    random.seed(rt.random_seed)
    if len(combos) > rt.max_variants:
        combos = random.sample(combos, rt.max_variants)

    os.makedirs(rt.out_dir, exist_ok=True)
    summary_rows: List[Dict[str, Any]] = []
    best_metric = -1e9
    best_payload: Optional[Dict[str, Any]] = None
    best_trades = pd.DataFrame()
    best_equity = pd.DataFrame()

    # Pre-load M1 for speed (other TF loads inside generate_signals)
    m1_df = load_df_for(base_cfg.symbol, "M1", base_cfg)
    if m1_df is None:
        raise RuntimeError("M1 data missing even after ensure_data")

    for idx, combo in enumerate(combos, start=1):
        cfg = replace(base_cfg, **combo)
        try:
            sigs = generate_signals(cfg)
        except Exception as e:
            print(f"[Variant {idx}] Failed param set {combo}: {e}")
            continue
        trades_df, eq_df, metrics = backtest_signals(sigs, m1_df, cfg, rt)
        metrics.update(combo)
        metrics["variant_id"] = idx
        metrics["signals"] = len(sigs)
        metrics["trades_pct_of_signals"] = (metrics.get("trades",0) / len(sigs)) if len(sigs) else 0
        summary_rows.append(metrics)
        viability = (metrics.get("trades",0) >= rt.min_trades_for_viable)
        expR = metrics.get("expectancy_R", -999)
        win_rate = metrics.get("win_rate",0)
        pf = metrics.get("profit_factor", 0) or 0
        sharpe = metrics.get("sharpe_R",0) if not np.isnan(metrics.get("sharpe_R", np.nan)) else 0
        # Composite score emphasizing expectancy & risk-adjusted performance
        score = (expR * 100) + (win_rate * 5) + (pf) + (0.5 * sharpe)
        if not viability:
            score *= 0.25  # penalize insufficient sample size
        if score > best_metric:
            best_metric = score
            best_payload = metrics
            best_trades = trades_df.copy()
            best_equity = eq_df.copy()
        if rt.save_all_trade_logs and not trades_df.empty:
            trades_path = os.path.join(rt.out_dir, f"variant_{idx}_trades.csv")
            trades_df.to_csv(trades_path, index=False)
        print(f"[Variant {idx}/{len(combos)}] trades={metrics.get('trades')} expR={metrics.get('expectancy_R'):.3f} win={metrics.get('win_rate'):.2%}")

    if not summary_rows:
        raise RuntimeError("No successful variants produced results")

    summary_df = pd.DataFrame(summary_rows)
    summary_df.sort_values(["expectancy_R","win_rate"], ascending=[False, False], inplace=True)
    summary_path = os.path.join(rt.out_dir, "variants_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    if best_payload is not None:
        best_trades.to_csv(os.path.join(rt.out_dir, "best_variant_trades.csv"), index=False)
        best_equity.to_csv(os.path.join(rt.out_dir, "equity_curve_best.csv"), index=False)
        if rt.save_equity_plot and plt is not None and not best_equity.empty:
            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(best_equity["time"], best_equity["equity"], label="Equity")
            ax.set_title("Equity Curve (Best Variant)")
            ax.set_xlabel("Time"); ax.set_ylabel("Equity")
            ax.grid(True, alpha=0.3)
            ax.legend()
            fig.autofmt_xdate()
            fig.savefig(os.path.join(rt.out_dir, rt.equity_plot_filename), dpi=130)
            plt.close(fig)

    return summary_df, best_payload or {}


# ---------------- Main Entry ----------------

def main():
    base_cfg = Config()
    ensure_data(base_cfg)  # synthesize if missing
    print("Running parameter sweep...")
    t0 = time.time()
    summary_df, best = run_parameter_grid(base_cfg, RUNTIME)
    elapsed = time.time() - t0
    print(f"Completed sweep in {elapsed:.1f}s | Variants evaluated: {summary_df.shape[0]}")
    if best:
        key_fields = [
            "variant_id","trades","wins","losses","win_rate","expectancy_R","profit_factor","net_profit","return_pct","max_drawdown_pct","CAGR","MAR","risk_of_ruin"
        ]
        print("Best variant summary:")
        for k in key_fields:
            if k in best:
                v = best[k]
                if isinstance(v, float):
                    if "win_rate" in k:
                        print(f"  {k}: {v:.2%}")
                    else:
                        print(f"  {k}: {v:.4f}")
                else:
                    print(f"  {k}: {v}")
        print("Parameter values:")
        for p in PARAM_GRID.keys():
            if p in best:
                print(f"  {p}: {best[p]}")
    else:
        print("No viable variant found.")
    print("Artifacts written to:", RUNTIME.out_dir)


if __name__ == "__main__":
    main()
