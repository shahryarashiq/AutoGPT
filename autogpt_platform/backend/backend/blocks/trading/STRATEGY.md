# Multi-Indicator Scalping Strategy for Forex and XAUUSD

## Strategy Overview

This strategy combines multiple technical indicators with smart money concepts (order blocks, breaker blocks, FVG) to identify high-probability trading opportunities with a target win rate of 60-70%.

**Target Markets:** Forex pairs (EUR/USD, GBP/USD, USD/JPY, etc.) and XAUUSD (Gold)  
**Timeframes:** M5 (entry), M15 (confirmation), H1 (trend)  
**Risk/Reward Ratio:** Minimum 1:2, Target 1:3  
**Expected Win Rate:** 60-70%  
**Account Size:** $100 starting capital  
**Trading Style:** Scalping with intraday holds

---

## Core Components

### 1. Trend Identification (H1 Timeframe)

**Primary Indicators:**
- **EMA 50 & EMA 200**: Trend direction
  - Bullish: Price > EMA 50 > EMA 200
  - Bearish: Price < EMA 50 < EMA 200
  
- **ADX (Average Directional Index)**: Trend strength
  - ADX > 25: Strong trend (trade with trend)
  - ADX < 20: Weak trend (avoid or reduce position size)

### 2. Momentum & Oscillators (M15 Timeframe)

**MACD (Moving Average Convergence Divergence):**
- Settings: 12, 26, 9
- Buy Signal: MACD crosses above signal line + histogram positive
- Sell Signal: MACD crosses below signal line + histogram negative
- Divergence detection for reversal trades

**RSI (Relative Strength Index):**
- Settings: 14 period
- Overbought: > 70 (prepare for shorts)
- Oversold: < 30 (prepare for longs)
- Ideal entry: RSI between 40-60 for trend continuation

**Stochastic Oscillator:**
- Settings: 14, 3, 3
- Confirmation: %K crosses %D in oversold/overbought zones

### 3. Volatility & Support/Resistance (M15 Timeframe)

**Bollinger Bands:**
- Settings: 20, 2
- Entry: Price bounces off lower band (buy) or upper band (sell)
- Breakout: Strong move through bands with volume confirmation

**ATR (Average True Range):**
- Settings: 14 period
- Used for:
  - Stop loss placement (1.5-2x ATR)
  - Take profit levels (3-4x ATR)
  - Position sizing based on volatility
  - Filter low volatility periods (avoid when ATR too low)

### 4. Smart Money Concepts (M5 & M15 Timeframes)

**Order Blocks (OB):**
- Definition: Last bullish/bearish candle before significant move
- Identification:
  - Bullish OB: Last green candle before price drops significantly
  - Bearish OB: Last red candle before price rises significantly
- Usage: Wait for price to return to OB for entry

**Breaker Blocks (BB):**
- Definition: Failed order block that becomes support/resistance
- Identification: OB that was broken and now acts as opposite zone
- Usage: High-probability reversal zones

**Fair Value Gaps (FVG):**
- Definition: Imbalance between three candles (gap in price action)
- Bullish FVG: Gap between candle 1 high and candle 3 low (upward move)
- Bearish FVG: Gap between candle 1 low and candle 3 high (downward move)
- Usage: Price typically returns to fill 50% of FVG

**Inverse Fair Value Gaps (IFVG):**
- Definition: FVG within FVG (nested imbalances)
- Usage: High-probability entries when price reaches IFVG

### 5. Key Levels (Daily & H4 Timeframes)

**Fibonacci Retracements:**
- Settings: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
- Applied to: Recent swing high/low
- Entry zones: 50%, 61.8% (golden pocket)
- Extension targets: 127.2%, 161.8%, 200%

**Pivot Points:**
- Classic Pivot Points: (High + Low + Close) / 3
- Levels: R3, R2, R1, PP, S1, S2, S3
- Usage: Support/resistance, profit targets

**Volume Profile:**
- Point of Control (POC): Highest volume level
- Value Area High/Low (VAH/VAL): 70% of volume
- Usage: Identify high-volume support/resistance zones

---

## Entry Rules

### LONG Entry Conditions (ALL must be met):

1. **Trend Confirmation (H1):**
   - Price > EMA 50 > EMA 200
   - ADX > 25

2. **Momentum (M15):**
   - MACD crossed above signal line (within last 3 candles)
   - RSI between 40-60 OR bouncing from oversold (<30)
   - Stochastic %K > %D in oversold zone

3. **Structure (M5/M15):**
   - Price at/near bullish order block OR
   - Price at/near FVG/IFVG fill zone OR
   - Price bounced off Bollinger lower band
   - No bearish breaker block above

4. **Key Levels:**
   - Price at Fibonacci 50% or 61.8% retracement OR
   - Price at support pivot (S1, S2) OR
   - Price at Volume Profile VAL or POC support

5. **Volume Confirmation:**
   - Increased volume on bullish candles
   - Volume above 20-period average

6. **Risk Management:**
   - ATR not too low (> 50% of 20-period ATR average)
   - Clear stop loss level identified

### SHORT Entry Conditions (ALL must be met):

1. **Trend Confirmation (H1):**
   - Price < EMA 50 < EMA 200
   - ADX > 25

2. **Momentum (M15):**
   - MACD crossed below signal line (within last 3 candles)
   - RSI between 40-60 OR dropping from overbought (>70)
   - Stochastic %K < %D in overbought zone

3. **Structure (M5/M15):**
   - Price at/near bearish order block OR
   - Price at/near FVG/IFVG fill zone OR
   - Price bounced off Bollinger upper band
   - No bullish breaker block below

4. **Key Levels:**
   - Price at Fibonacci 50% or 61.8% retracement OR
   - Price at resistance pivot (R1, R2) OR
   - Price at Volume Profile VAH or POC resistance

5. **Volume Confirmation:**
   - Increased volume on bearish candles
   - Volume above 20-period average

6. **Risk Management:**
   - ATR not too low (> 50% of 20-period ATR average)
   - Clear stop loss level identified

---

## Exit Rules

### Stop Loss Placement:

1. **Primary Method:** 
   - Below/above recent swing low/high
   - Minimum: 1.5x ATR from entry
   - Maximum: 2.5x ATR from entry

2. **Alternative Methods:**
   - Below/above order block
   - Below/above FVG zone
   - Below/above key Fibonacci level

### Take Profit Targets:

**Target 1 (40% of position):**
- Risk/Reward: 1:1.5
- Location: 
  - Previous swing high/low
  - Fibonacci 23.6% extension
  - Pivot point level (R1/S1)

**Target 2 (40% of position):**
- Risk/Reward: 1:2.5
- Location:
  - Major resistance/support
  - Fibonacci 50% extension
  - Pivot point level (R2/S2)
  - Volume Profile POC

**Target 3 (20% of position):**
- Risk/Reward: 1:4
- Location:
  - Fibonacci 100% extension
  - Major psychological levels
  - Daily high/low

### Trailing Stop:

- Activate after Target 1 hit
- Trail by 1x ATR below recent swing low/high
- Lock in minimum 1:2 RR after Target 2 hit

---

## Position Sizing & Risk Management

### Initial Risk Parameters:

- **Maximum Risk Per Trade:** 2% of account balance
- **Maximum Daily Risk:** 6% of account balance
- **Maximum Open Positions:** 3 trades simultaneously
- **Maximum Drawdown:** 15% (stop trading, review strategy)

### Position Sizing Formula:

```
Lot Size = (Account Balance × Risk %) / (Stop Loss in Pips × Pip Value)
```

### Compounding Strategy:

**After Winning Trade:**
- If account grows by 5%: Increase risk per trade by 0.1%
- If account grows by 10%: Increase risk per trade by 0.2%
- Maximum risk per trade: 3% (reached at 50% account growth)

**After Losing Trade:**
- If 2 consecutive losses: Reduce risk to 1.5%
- If 3 consecutive losses: Reduce risk to 1%
- If 4 consecutive losses: Stop trading for the day
- Reset to 2% after 2 consecutive wins

**Dynamic Lot Size Calculation:**

```python
# Example for $100 account
account_balance = 100
risk_percent = 2  # 2% risk
stop_loss_pips = 20  # Based on ATR

# For Forex (1 micro lot = $0.10 per pip)
risk_amount = account_balance * (risk_percent / 100)  # $2
lot_size = risk_amount / (stop_loss_pips * 0.10)  # 1 micro lot

# For XAUUSD (1 micro lot = $0.01 per point)
# Adjust pip value accordingly
```

---

## Trade Management Rules

### Scaling In (Pyramiding):

- **Only with winning trades:** Add position when price moves 1x ATR in profit
- **Maximum additions:** 2 additional positions
- **Each addition:** 50% of initial position size
- **Requirement:** Each addition must have same or better RR ratio

### Scaling Out (Partial Profits):

- As described in Take Profit Targets
- Always take partial profits at key levels
- Never let winning trade turn into loser

### Break-Even Management:

- Move stop to break-even + spread when:
  - Price moves 1.5x initial risk in profit
  - Target 1 is hit
- Protects capital while letting winners run

---

## Session-Based Trading

### Best Trading Times (UTC):

**London Session (08:00-16:00 UTC):**
- EUR/USD, GBP/USD, EUR/GBP
- Highest volatility
- Best for scalping

**New York Session (13:00-21:00 UTC):**
- All major pairs
- USD pairs most active
- Overlap with London (13:00-16:00) = best opportunities

**Asian Session (00:00-08:00 UTC):**
- Avoid (low volatility, wide spreads)
- Exception: USD/JPY, AUD/JPY

### Days to Trade:

- **Best:** Tuesday, Wednesday, Thursday
- **Avoid:** Monday (week opening, unpredictable), Friday (week closing, early exits)
- **Never trade:** During major news events (NFP, FOMC, GDP, etc.)

---

## Fundamental Analysis Integration

### Economic Calendar Monitoring:

**High Impact News (Avoid trading 30 min before/after):**
- Non-Farm Payrolls (NFP)
- Federal Reserve Decisions (FOMC)
- GDP Reports
- Inflation Data (CPI, PPI)
- Central Bank Speeches
- Employment Data

**Medium Impact News (Reduce position size):**
- Retail Sales
- Manufacturing PMI
- Consumer Confidence
- Trade Balance

### Fundamental Bias:

**Consider overall economic conditions:**
- Interest rate differentials (higher rates = stronger currency)
- Economic growth indicators (GDP, employment)
- Central bank policy (hawkish vs dovish)
- Geopolitical events
- Risk sentiment (risk-on = sell USD/JPY, risk-off = buy USD/JPY)

**For XAUUSD (Gold):**
- Inverse relationship with USD
- Safe-haven in uncertainty
- Influenced by real yields, inflation expectations
- Watch DXY (Dollar Index) correlation

---

## Backtesting Methodology

### Data Requirements:

- **Historical Data:** Minimum 2 years, tick data preferred
- **Timeframes:** M5, M15, H1, H4, D1
- **Assets:** EUR/USD, GBP/USD, USD/JPY, XAUUSD
- **Include:** Spread costs, commission, slippage

### Performance Metrics:

**Target Metrics:**
- Win Rate: 60-70%
- Average RR: 1:2.5
- Profit Factor: > 2.0
- Maximum Drawdown: < 15%
- Sharpe Ratio: > 1.5
- Recovery Factor: > 3.0

**Monthly Target:**
- Account Growth: 10-20% per month
- Average Trades: 40-60 per month
- Average Win: $5-10 per trade (scales with account)

### Backtesting Process:

1. **Strategy Coding:** Implement all rules in Python/MQL5
2. **Initial Test:** Run on 1 year historical data
3. **Optimization:** Adjust indicator parameters if needed
4. **Walk-Forward Test:** Test on next 6 months (unseen data)
5. **Monte Carlo Analysis:** Test robustness with random entries
6. **Live Simulation:** Forward test on demo account for 1 month

---

## Strategy Scoring System

### Entry Quality Score (0-100):

Calculate score based on conditions met:
- Trend alignment (H1): 20 points
- MACD signal: 15 points
- RSI optimal range: 15 points
- Order block/FVG alignment: 20 points
- Fibonacci level: 10 points
- Volume confirmation: 10 points
- Pivot/support alignment: 10 points

**Minimum score to trade:** 70/100
**High confidence trade:** 85+/100

### Risk Management Score:

- Clear stop loss: 25 points
- RR ratio > 1:2: 25 points
- ATR sufficient: 20 points
- Within daily risk limits: 15 points
- Not in news event window: 15 points

**Minimum score to trade:** 80/100

---

## Implementation Notes

### MetaTrader 5 Python Integration:

```python
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime

# Initialize MT5
if not mt5.initialize():
    print("MT5 initialization failed")
    mt5.shutdown()

# Key functions needed:
# 1. mt5.copy_rates_range() - Get historical data
# 2. mt5.symbol_info_tick() - Get current prices
# 3. mt5.order_send() - Place trades
# 4. mt5.positions_get() - Get open positions
# 5. mt5.account_info() - Get account information
```

### Indicator Calculation Libraries:

- **TA-Lib:** Comprehensive technical analysis library
- **Pandas TA:** Python pandas extension for TA
- **Custom:** Order blocks, FVG, breaker blocks (manual implementation)

### Required Data Structures:

```python
# Trade signal structure
signal = {
    'action': 'buy' | 'sell' | 'none',
    'confidence': 0-100,
    'entry_price': float,
    'stop_loss': float,
    'take_profit_1': float,
    'take_profit_2': float,
    'take_profit_3': float,
    'position_size': float,
    'reason': str,  # Why trade was taken
}
```

---

## Expected Performance

### Conservative Estimate:

Starting with $100:
- **Month 1:** 10-15% growth → $110-115
- **Month 2:** 12-18% growth → $123-136
- **Month 3:** 15-20% growth → $142-163
- **Month 6:** Account: $200-300
- **Month 12:** Account: $450-750

### Risk Considerations:

- Slippage on small account: 0.5-1 pip average
- Spread costs: Account for in TP/SL calculations
- Broker limitations: Minimum lot size, maximum leverage
- Psychological factors: Stick to plan, avoid over-trading

### Failure Modes & Solutions:

**Problem:** Low win rate (<50%)
**Solution:** Increase entry score threshold, reduce trading frequency

**Problem:** Good win rate but losing money
**Solution:** Check RR ratio, improve TP placement

**Problem:** Frequent stop outs
**Solution:** Wider stops based on ATR, better entry timing

**Problem:** Overtrading
**Solution:** Implement max trades per day limit (5-7)

---

## Next Steps for Implementation

1. **Code the indicator calculations** (EMA, MACD, RSI, ATR, etc.)
2. **Implement smart money concepts** (OB, FVG detection algorithms)
3. **Build entry/exit signal generator**
4. **Create risk management module** (position sizing, compounding)
5. **Develop MT5 integration** (data fetching, order execution)
6. **Build backtesting framework**
7. **Optimize parameters** on historical data
8. **Forward test** on demo account
9. **Deploy to live trading** with strict monitoring

---

## Disclaimer

**This strategy is for educational purposes. Past performance does not guarantee future results. Trading forex and gold involves substantial risk of loss. Only trade with money you can afford to lose. Always test thoroughly on demo accounts before live trading.**
