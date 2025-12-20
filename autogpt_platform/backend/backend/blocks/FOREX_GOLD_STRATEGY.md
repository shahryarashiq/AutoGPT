# Forex and Gold Trading Strategy Block

## Overview

This block implements a comprehensive trading strategy for **Forex** and **Gold** markets using both **technical analysis** and **fundamental analysis** to generate high-probability trading signals with a target win rate of **60%+**.

## Features

### Technical Analysis Indicators

The block implements the following technical indicators:

1. **RSI (Relative Strength Index)**
   - Identifies overbought and oversold conditions
   - Default period: 14
   - Oversold level: 30
   - Overbought level: 70

2. **MACD (Moving Average Convergence Divergence)**
   - Trend-following momentum indicator
   - Fast period: 12
   - Slow period: 26
   - Signal period: 9

3. **Moving Averages (SMA/EMA)**
   - Identifies trend direction and crossovers
   - Short-term MA: 20 periods
   - Long-term MA: 50 periods

4. **Bollinger Bands**
   - Measures volatility and price levels
   - Period: 20
   - Standard deviation: 2.0

5. **ATR (Average True Range)**
   - Measures market volatility
   - Used for calculating stop-loss and take-profit levels
   - Period: 14

6. **Stochastic Oscillator**
   - Momentum indicator comparing closing price to price range
   - %K period: 14
   - %D period: 3

### Fundamental Analysis

The block also supports fundamental analysis including:

- **Economic Calendar Events** - High/medium/low impact events
- **News Sentiment Analysis** - Positive/negative/neutral sentiment
- **Market Correlation** - Cross-market analysis

### Signal Generation

The strategy combines technical and fundamental analysis with the following weights:
- **70% Technical Analysis** - Based on multiple indicator consensus
- **30% Fundamental Analysis** - Based on news and economic events

Signals are generated when:
- **BUY Signal**: Combined score > 0.1 and confidence >= threshold
- **SELL Signal**: Combined score < -0.1 and confidence >= threshold
- **HOLD Signal**: When confidence is below threshold or signals are mixed

### Risk Management

The block automatically calculates:
- **Entry Price** - Recommended entry point
- **Stop Loss** - Based on ATR (2x ATR from entry)
- **Take Profit** - Based on risk-reward ratio (configurable, default 2:1)

## Usage

### Basic Usage

```json
{
  "market_type": "Forex",
  "symbol": "EURUSD",
  "timeframe": "1 Hour",
  "price_data": [
    {"open": 1.1000, "high": 1.1050, "low": 1.0950, "close": 1.1020, "volume": 1000},
    {"open": 1.1020, "high": 1.1070, "low": 1.1000, "close": 1.1060, "volume": 1100}
  ],
  "confidence_threshold": 0.6
}
```

### Advanced Usage with Fundamental Analysis

```json
{
  "market_type": "Forex",
  "symbol": "EURUSD",
  "timeframe": "1 Hour",
  "price_data": [...],
  "use_fundamental_analysis": true,
  "economic_events": [
    {"name": "Interest Rate Decision", "impact": "high"},
    {"name": "NFP", "impact": "high"}
  ],
  "news_sentiment": "positive",
  "confidence_threshold": 0.6,
  "risk_reward_ratio": 2.0
}
```

### Gold Market Example

```json
{
  "market_type": "Gold",
  "symbol": "XAUUSD",
  "timeframe": "4 Hours",
  "price_data": [...],
  "confidence_threshold": 0.65,
  "risk_reward_ratio": 2.5
}
```

## Inputs

### Required Inputs

- **market_type**: Select Forex or Gold
- **symbol**: Trading pair (e.g., EURUSD, GBPUSD, XAUUSD)
- **timeframe**: Select from 1M, 5M, 15M, 30M, 1H, 4H, 1D, 1W
- **price_data**: List of price bars with OHLC data

### Optional Inputs

- **use_rsi**: Enable/disable RSI indicator (default: true)
- **use_macd**: Enable/disable MACD indicator (default: true)
- **use_moving_averages**: Enable/disable MA indicator (default: true)
- **use_bollinger_bands**: Enable/disable Bollinger Bands (default: true)
- **use_atr**: Enable/disable ATR indicator (default: true)
- **use_stochastic**: Enable/disable Stochastic Oscillator (default: true)
- **use_fundamental_analysis**: Enable/disable fundamental analysis (default: true)
- **confidence_threshold**: Minimum confidence for signals (default: 0.6)
- **risk_reward_ratio**: Target risk-reward ratio (default: 2.0)

### Advanced Parameters

Each indicator has customizable parameters:
- RSI: period, oversold level, overbought level
- MACD: fast, slow, signal periods
- MA: short and long periods
- Bollinger Bands: period, standard deviation
- ATR: period
- Stochastic: %K and %D periods

## Outputs

- **signal**: Trading signal (BUY, SELL, or HOLD)
- **confidence**: Confidence level (0-1)
- **entry_price**: Recommended entry price
- **stop_loss**: Stop loss level
- **take_profit**: Take profit level
- **technical_analysis**: Detailed technical indicator values
- **fundamental_analysis**: Fundamental analysis results
- **strategy_explanation**: Human-readable explanation of the signal

## Strategy Logic

### Multi-Indicator Consensus

The strategy uses a consensus approach:

1. Each enabled indicator contributes a score (-1 to +1)
2. Scores are weighted and combined
3. Final score determines signal direction
4. Confidence is based on indicator agreement

### Example Signal Generation

**Bullish Scenario:**
- RSI < 30 (oversold) → +0.2
- MACD histogram > 0 → +0.15
- Short MA > Long MA → +0.2
- Price < Lower Bollinger Band → +0.15
- Stochastic < 20 → +0.1
- Positive news sentiment → +0.3 (fundamental)

Total Score: 0.8 → **Strong BUY Signal**

**Bearish Scenario:**
- RSI > 70 (overbought) → -0.2
- MACD histogram < 0 → -0.15
- Short MA < Long MA → -0.2
- Price > Upper Bollinger Band → -0.15
- Stochastic > 80 → -0.1
- Negative news sentiment → -0.3 (fundamental)

Total Score: -0.8 → **Strong SELL Signal**

## Target Win Rate

The strategy aims for a **60%+ win rate** by:

1. **Multi-indicator confirmation** - Reduces false signals
2. **Fundamental analysis integration** - Filters trades during high-impact events
3. **Risk management** - Uses proper stop-loss and take-profit levels
4. **Confidence threshold** - Only trades when confidence is high
5. **Adaptive parameters** - Customizable for different market conditions

## Best Practices

### For Forex Trading

- Use 1H or 4H timeframes for swing trading
- Use 15M or 30M for intraday trading
- Set confidence threshold to 0.6 or higher
- Monitor economic calendar events
- Consider currency correlations

### For Gold Trading

- Gold is more volatile - adjust confidence threshold to 0.65+
- Use 4H or 1D timeframes for trend following
- Pay attention to USD strength and inflation data
- Use wider stop-loss levels due to higher volatility
- Consider risk-reward ratio of 2.5:1 or higher

### Risk Management Tips

1. Never risk more than 1-2% of capital per trade
2. Always use stop-loss orders
3. Take partial profits at 1:1 risk-reward
4. Trail stop-loss after reaching 1.5:1
5. Avoid trading during major news events (unless specifically analyzed)

## Example Workflow in AutoGPT Platform

1. **Data Collection Block** → Fetch price data from API
2. **Forex/Gold Strategy Block** → Analyze and generate signal
3. **Decision Block** → Check if signal is BUY or SELL
4. **Trading Block** → Execute trade with calculated levels
5. **Notification Block** → Send trade notification

## Limitations

- Requires minimum 3 price bars (preferably 50+ for accurate indicators)
- Past performance does not guarantee future results
- Should be used with proper risk management
- Fundamental analysis requires external data sources
- Win rate depends on market conditions and parameters

## Support

For issues, questions, or feature requests, please refer to the AutoGPT documentation or create an issue in the repository.

## Block ID

`a7f3e2c1-9b4d-4e8f-a1c5-7d6e8f9a0b1c`
