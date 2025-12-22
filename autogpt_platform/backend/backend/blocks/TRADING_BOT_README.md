# Trading Bot Block

## Quick Start

This trading bot provides comprehensive technical analysis for Forex and Gold (XAU/USD) trading with a focus on scalping strategies.

### Installation

The trading bot is automatically loaded as a block in the AutoGPT platform. No additional installation is required.

### Basic Usage

1. **In the AutoGPT Platform UI**:
   - Add the "Trading Bot" block to your workflow
   - Configure the trading pair (e.g., XAU/USD, EUR/USD)
   - Select timeframe (M5, M15, M30 recommended for scalping)
   - Provide price data (connect to a data source block)
   - Set account balance and risk percentage

2. **Programmatically**:
```python
from backend.blocks.trading_bot import TradingBotBlock

# Create instance
bot = TradingBotBlock()

# Prepare input
input_data = {
    "pair": "XAUUSD",
    "timeframe": "15min",
    "prices": [2050.0, 2050.5, 2051.0, ...],  # Your price data
    "highs": [2051.5, 2052.0, 2052.5, ...],   # Optional
    "lows": [2049.5, 2050.0, 2050.5, ...],    # Optional
    "account_balance": 10000.0,
    "risk_per_trade": 1.5
}

# Run analysis
results = {}
async for key, value in bot.run(bot.Input(**input_data)):
    results[key] = value

print(f"Signal: {results['signal']}")
print(f"Confidence: {results['confidence']}%")
```

### Example Output

```
Signal: BUY
Confidence: 85.0%
Entry Price: 2075.50
Stop Loss: 2072.00
Take Profit: 2084.25
Risk/Reward: 2.5:1
Position Size: 0.28
```

## Features

- **Technical Indicators**: EMA, RSI, MACD, Bollinger Bands, ATR
- **Risk Management**: Automatic position sizing and stop loss calculation
- **Confidence Scoring**: Each signal includes a confidence level
- **Multi-Pair Support**: Forex majors and Gold (XAU/USD)
- **Scalping Optimized**: Designed for M5-M30 timeframes

## Strategy Details

The bot uses a point-based scoring system that requires confluence of multiple indicators:

### Signal Requirements
- **Minimum Score**: 60 points (out of 100)
- **Trend Analysis**: 30 points
- **Momentum**: 25 points (RSI)
- **MACD Confirmation**: 25 points
- **Entry Trigger**: 20 points (Bollinger Bands)

### Risk Management
- **Stop Loss**: 1.5x ATR from entry
- **Take Profit**: 2.5x stop loss distance (2.5:1 R/R)
- **Position Sizing**: Based on account balance and risk percentage

## Performance Expectations

**Target Metrics**:
- Win Rate: 60-70%
- Risk/Reward: 1:2 or better
- Best Timeframe: M15 (15 minutes)
- Best Pairs: EUR/USD, XAU/USD

**Note**: These are targets based on strategy design. Actual performance depends on market conditions and execution.

## Integration Examples

### With MetaTrader 5

```python
import MetaTrader5 as mt5

# Get live data from MT5
mt5.initialize()
rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_M15, 0, 250)
closes = [rate[4] for rate in rates]

# Run analysis
# ... use trading bot with closes
mt5.shutdown()
```

### With OANDA API

```python
import oandapyV20

# Fetch candles from OANDA
# ... (see examples/trading_bot_example.py for full code)
```

### Backtesting with yfinance

```python
import yfinance as yf

# Download historical data
gold = yf.download('GC=F', period='1mo', interval='15m')
closes = gold['Close'].tolist()

# Run analysis
# ... use trading bot with closes
```

## Important Warnings

⚠️ **DISCLAIMER**: Trading involves substantial risk of loss.

### Before Live Trading:
1. **Backtest thoroughly** (minimum 3 months of historical data)
2. **Paper trade** (test without real money)
3. **Demo account** (test with broker's demo)
4. **Small positions** (start with minimum size)
5. **Understand risks** (never risk money you can't afford to lose)

### Limitations:
- This is **analysis only**, not a complete trading system
- Requires integration with broker API for execution
- Does not account for slippage, spreads, or commissions
- Past performance does not guarantee future results

## Configuration

### Customizing Indicators

Edit `trading_bot.py` to adjust:
- RSI period (default: 14)
- EMA periods (default: 20, 50, 200)
- Bollinger Bands parameters (default: 20 period, 2 std dev)
- ATR multiplier for stops (default: 1.5x)
- Risk/Reward ratio (default: 2.5:1)

### Optimizing for Different Markets

**For Forex Major Pairs**:
- Use M15 or M30 timeframes
- Lower risk per trade (1-1.5%)
- Trade during London/NY overlap

**For Gold (XAU/USD)**:
- Allow wider stops (higher volatility)
- Use smaller position sizes
- Best liquidity during London/NY sessions

**For Aggressive Scalping**:
- Use M5 timeframe
- Increase monitoring frequency
- Reduce position size

## Testing

Run the example script:
```bash
cd autogpt_platform/backend
python -m backend.blocks.examples.trading_bot_example
```

Run block tests:
```bash
poetry run pytest backend/blocks/test/test_block.py::test_available_blocks[TradingBotBlock] -xvs
```

## Documentation

Full documentation: `/docs/content/platform/blocks/trading_bot.md`

## Support

For issues or questions:
1. Check the full documentation
2. Review examples in `examples/trading_bot_example.py`
3. Test with demo data first
4. Join the AutoGPT Discord for community support

## License

This block is part of the AutoGPT platform and follows the repository's license terms.

---

**Remember**: Always test thoroughly before risking real capital. Trading is risky, and losses can exceed deposits.
