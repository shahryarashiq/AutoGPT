# Trading Bot Documentation

## Overview

The Trading Bot block is an advanced trading analysis tool for Forex and XAU/USD (Gold) markets. It implements a comprehensive scalping strategy designed to achieve 60-70% win rate with proper risk management.

## Features

### Multi-Indicator Technical Analysis
- **EMA (Exponential Moving Average)**: 20, 50, and 200 periods for trend identification
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Momentum confirmation
- **Bollinger Bands**: Volatility analysis and entry point identification
- **ATR (Average True Range)**: Dynamic stop loss placement based on volatility

### Strategy Logic

The bot uses a point-based scoring system to generate trading signals:

#### BUY Signal Criteria
- Uptrend confirmed (EMA 20 > EMA 50 > EMA 200): 30 points
- RSI oversold or favorable (<45): 25 points
- MACD bullish crossover: 25 points
- Price at lower Bollinger Band: 20 points
- **Minimum score required: 60 points**

#### SELL Signal Criteria
- Downtrend confirmed (EMA 20 < EMA 50 < EMA 200): 30 points
- RSI overbought or favorable (>55): 25 points
- MACD bearish crossover: 25 points
- Price at upper Bollinger Band: 20 points
- **Minimum score required: 60 points**

### Risk Management

- **Dynamic Position Sizing**: Calculated based on account balance and risk percentage
- **ATR-Based Stop Loss**: 1.5x ATR for adaptive risk control
- **Risk/Reward Ratio**: Minimum 2.5:1 (configurable)
- **Confidence Scoring**: Each signal includes confidence level (0-100%)

## Supported Trading Pairs

### Forex Majors
- EUR/USD
- GBP/USD
- USD/JPY
- USD/CHF
- AUD/USD
- USD/CAD
- NZD/USD

### Precious Metals
- XAU/USD (Gold)

## Recommended Timeframes

- **M5 (5 minutes)**: Aggressive scalping
- **M15 (15 minutes)**: Recommended for balanced approach
- **M30 (30 minutes)**: Conservative scalping
- **H1 (1 hour)**: Swing trading

## Usage Example

### Input Configuration

```json
{
  "pair": "XAUUSD",
  "timeframe": "15min",
  "prices": [2050.0, 2050.5, 2051.0, ...],  // Minimum 50 points, 200+ recommended
  "highs": [2051.5, 2052.0, 2052.5, ...],    // Optional, uses prices if not provided
  "lows": [2049.5, 2050.0, 2050.5, ...],     // Optional, uses prices if not provided
  "account_balance": 10000.0,
  "risk_per_trade": 1.0  // 1% risk per trade
}
```

### Output Structure

```json
{
  "signal": "BUY",
  "pair": "XAUUSD",
  "timeframe": "15min",
  "confidence": 85.0,
  "entry_price": 2075.50,
  "stop_loss": 2072.00,
  "take_profit": 2084.25,
  "risk_reward_ratio": 2.5,
  "position_size": 0.28,
  "risk_amount": 100.0,
  "indicators": {
    "ema_20": 2074.80,
    "ema_50": 2072.50,
    "ema_200": 2070.00,
    "rsi": 42.5,
    "macd": {
      "macd": 1.25,
      "signal": 0.85,
      "histogram": 0.40
    },
    "bollinger_bands": {
      "upper": 2080.00,
      "middle": 2075.00,
      "lower": 2070.00
    },
    "atr": 2.33,
    "current_price": 2075.50
  },
  "analysis": "Uptrend confirmed (EMA alignment) | RSI favorable for buy (42.5) | MACD bullish crossover",
  "timestamp": "2025-12-22T14:30:00.000000"
}
```

## Integration with Trading Platforms

### MetaTrader 5 (MT5)

To connect this analysis block with MT5 for actual trading:

1. Use the HTTP block to send signals to an MT5 Python API bridge
2. Example bridge: [mt5-python-rest-api](https://github.com/RoboTradeCode/mt5-python-rest-api)

### OANDA

Connect using OANDA's REST API:

1. Get OANDA API credentials
2. Use HTTP block to fetch price data
3. Send orders based on trading signals

### Interactive Brokers

Use the IB Gateway with [ib_insync](https://github.com/erdewit/ib_insync):

1. Set up IB Gateway
2. Connect through REST API bridge
3. Execute trades based on signals

## Best Practices

### Data Requirements
- **Minimum**: 50 data points
- **Recommended**: 200+ data points for accurate indicator calculation
- **Update Frequency**: Match your chosen timeframe (e.g., every 15 minutes for M15)

### Risk Management
- Never risk more than 1-2% of account per trade
- Use the calculated stop loss - don't modify it
- Respect the risk/reward ratio
- Don't trade when confidence is below 70%

### Market Conditions
- Best performance in trending markets
- Reduced performance in ranging/choppy markets
- Avoid trading during major news events
- Be cautious during low liquidity periods (Asian session for Forex)

### Scalping Tips
1. **For M5/M15 timeframes**:
   - Quick entry and exit
   - Monitor positions actively
   - Use tighter stops on Gold due to higher volatility

2. **For Forex pairs**:
   - EUR/USD and GBP/USD offer best liquidity
   - Avoid exotic pairs with high spreads
   - Trade during London/NY session overlap

3. **For XAU/USD (Gold)**:
   - Higher volatility = larger stops needed
   - Consider smaller position sizes
   - Best liquidity during London and NY sessions

## Performance Optimization

### Achieving 60-70% Win Rate

1. **Signal Selection**:
   - Only trade signals with 70%+ confidence
   - Wait for confluence of at least 3 indicators

2. **Timeframe Selection**:
   - M15 offers best balance for scalping
   - Use higher timeframes for confirmation

3. **Market Selection**:
   - Focus on 2-3 pairs you know well
   - Gold (XAU/USD) offers explosive moves
   - Major Forex pairs offer consistency

4. **Session Timing**:
   - Avoid trading during first/last hour of sessions
   - Best setups during active market hours
   - Avoid trading between 22:00-2:00 UTC (low liquidity)

## Backtesting

To backtest this strategy:

1. Collect historical data (200+ candles per test)
2. Run the block on each candle close
3. Track entry, exit, and results
4. Calculate win rate and profit factor
5. Optimize parameters if needed

### Sample Backtest Metrics

Target metrics for validation:
- **Win Rate**: 60-70%
- **Risk/Reward**: 1:2 or better
- **Profit Factor**: >1.5
- **Max Drawdown**: <15%

## Limitations and Disclaimers

### Important Warnings

⚠️ **RISK DISCLAIMER**: Trading involves substantial risk of loss. This tool is for educational and analysis purposes only.

### Limitations

1. **Not a Complete Trading System**: This block only provides analysis. You need:
   - Broker integration
   - Order execution system
   - Real-time data feed
   - Account management

2. **Past Performance**: Historical performance does not guarantee future results

3. **Market Conditions**: Strategy performance varies with market conditions

4. **Slippage and Costs**: Real trading includes:
   - Broker spreads
   - Commissions
   - Slippage
   - Overnight financing costs

5. **Emotional Factors**: Automated analysis doesn't account for:
   - Trader psychology
   - Discipline requirements
   - Risk tolerance variations

### Recommended Testing Process

1. **Paper Trading**: Test without real money (minimum 3 months)
2. **Demo Account**: Test with broker's demo account
3. **Small Live**: Start with minimum position sizes
4. **Gradual Scaling**: Increase size only after consistent results

## Advanced Configuration

### Customizing Indicator Parameters

You can modify the strategy by editing `trading_bot.py`:

```python
# Example: Adjust RSI sensitivity
rsi = self.indicators.calculate_rsi(prices, 14)  # Default
rsi = self.indicators.calculate_rsi(prices, 10)  # More sensitive

# Example: Adjust risk/reward ratio
take_profit = entry_price + (stop_distance * 2.5)  # Default 2.5:1
take_profit = entry_price + (stop_distance * 3.0)  # More aggressive 3:1
```

### Multi-Timeframe Analysis

For improved accuracy, analyze multiple timeframes:

1. Use H1/H4 for trend direction
2. Use M15/M30 for entry timing
3. Combine signals from both

## Support and Resources

### Learning Resources

- [BabyPips School of Pips](https://www.babypips.com/learn/forex) - Free Forex education
- [Investopedia Trading Guide](https://www.investopedia.com/trading-4427765)
- [TradingView](https://www.tradingview.com/) - Charts and analysis

### Technical Indicators References

- [RSI Explained](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Guide](https://www.investopedia.com/terms/m/macd.asp)
- [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- [ATR Guide](https://www.investopedia.com/terms/a/atr.asp)

## Troubleshooting

### Common Issues

1. **"Insufficient price data" error**:
   - Ensure at least 50 price points
   - Verify data format is correct (list of floats)

2. **Confidence always low**:
   - Check if market is ranging (no clear trend)
   - Verify price data is recent and accurate
   - Consider using different timeframe

3. **Signal says HOLD**:
   - Market conditions unclear
   - Waiting for better setup
   - This is normal and safe

4. **Position size seems wrong**:
   - Verify account balance is correct
   - Check risk percentage (should be 1-2%)
   - For Forex, remember position is in lots

## Changelog

### Version 1.0.0 (Initial Release)
- Multi-indicator technical analysis
- Support for major Forex pairs and Gold
- Automatic risk management
- Position sizing calculator
- Confidence scoring system
- Comprehensive documentation

## Contributing

To improve this trading bot:

1. Backtest with historical data
2. Report results and edge cases
3. Suggest indicator improvements
4. Share optimization findings

## License

This block is part of the AutoGPT platform and follows the repository's license terms.

---

**Remember**: Trading is risky. Never trade with money you can't afford to lose. Always test thoroughly before live trading.
