#!/usr/bin/env python3
"""
Trading Bot Example Usage

This script demonstrates how to use the Trading Bot block for Forex and Gold trading analysis.
It shows how to:
1. Fetch real market data (simulated here)
2. Analyze multiple trading pairs
3. Generate trading signals
4. Display results in a user-friendly format

To use with real data, integrate with:
- MetaTrader 5 (MT5) Python API
- OANDA API
- Interactive Brokers API
- yfinance for historical data
"""

import asyncio
from datetime import datetime, timedelta
from typing import List

# Simulated market data generator
def generate_sample_prices(
    base_price: float, num_points: int = 200, trend: str = "up"
) -> tuple[List[float], List[float], List[float]]:
    """
    Generate sample price data for testing
    
    Args:
        base_price: Starting price
        num_points: Number of data points to generate
        trend: "up", "down", or "sideways"
    
    Returns:
        Tuple of (closes, highs, lows)
    """
    import random
    
    closes = []
    highs = []
    lows = []
    
    current_price = base_price
    
    for i in range(num_points):
        # Add trend
        if trend == "up":
            trend_move = random.uniform(0.0001, 0.0005)
        elif trend == "down":
            trend_move = random.uniform(-0.0005, -0.0001)
        else:  # sideways
            trend_move = random.uniform(-0.0002, 0.0002)
        
        # Add noise
        noise = random.uniform(-0.0003, 0.0003)
        current_price = current_price * (1 + trend_move + noise)
        
        # Generate OHLC
        volatility = current_price * 0.0002
        high = current_price + random.uniform(0, volatility)
        low = current_price - random.uniform(0, volatility)
        
        closes.append(current_price)
        highs.append(high)
        lows.append(low)
    
    return closes, highs, lows


async def analyze_pair(pair: str, timeframe: str, trend: str = "up"):
    """Analyze a single trading pair"""
    from backend.blocks.trading_bot import TradingBotBlock
    
    # Base prices for different pairs
    base_prices = {
        "EURUSD": 1.0850,
        "GBPUSD": 1.2650,
        "USDJPY": 148.50,
        "XAUUSD": 2075.50,
        "AUDUSD": 0.6550,
    }
    
    base_price = base_prices.get(pair, 1.0000)
    
    # Generate sample data
    closes, highs, lows = generate_sample_prices(base_price, 250, trend)
    
    # Create block instance
    bot = TradingBotBlock()
    
    # Prepare input
    input_data = {
        "pair": pair,
        "timeframe": timeframe,
        "prices": closes,
        "highs": highs,
        "lows": lows,
        "account_balance": 10000.0,
        "risk_per_trade": 1.5,
    }
    
    # Run analysis
    results = {}
    async for key, value in bot.run(bot.Input(**input_data)):
        results[key] = value
    
    return results


def format_signal_output(pair: str, results: dict):
    """Format signal output for display"""
    
    print(f"\n{'='*60}")
    print(f"Trading Analysis: {pair}")
    print(f"{'='*60}")
    print(f"Timestamp: {results.get('timestamp', 'N/A')}")
    print(f"Timeframe: {results.get('timeframe', 'N/A')}")
    print(f"\n{'Signal':<20} {results.get('signal', 'N/A')}")
    print(f"{'Confidence':<20} {results.get('confidence', 0):.1f}%")
    
    signal = results.get('signal', 'HOLD')
    
    if signal != 'HOLD':
        print(f"\n--- Trade Parameters ---")
        print(f"{'Entry Price':<20} {results.get('entry_price', 0):.5f}")
        print(f"{'Stop Loss':<20} {results.get('stop_loss', 0):.5f}")
        print(f"{'Take Profit':<20} {results.get('take_profit', 0):.5f}")
        print(f"{'Risk/Reward':<20} {results.get('risk_reward_ratio', 0):.2f}:1")
        print(f"{'Position Size':<20} {results.get('position_size', 0):.4f}")
        print(f"{'Risk Amount':<20} ${results.get('risk_amount', 0):.2f}")
        
        # Calculate potential profit/loss
        if signal == 'BUY':
            potential_profit = (
                results.get('take_profit', 0) - results.get('entry_price', 0)
            ) * results.get('position_size', 0)
            potential_loss = (
                results.get('entry_price', 0) - results.get('stop_loss', 0)
            ) * results.get('position_size', 0)
        else:  # SELL
            potential_profit = (
                results.get('entry_price', 0) - results.get('take_profit', 0)
            ) * results.get('position_size', 0)
            potential_loss = (
                results.get('stop_loss', 0) - results.get('entry_price', 0)
            ) * results.get('position_size', 0)
        
        print(f"\n{'Potential Profit':<20} ${potential_profit:.2f}")
        print(f"{'Potential Loss':<20} ${potential_loss:.2f}")
    
    print(f"\n--- Technical Indicators ---")
    indicators = results.get('indicators', {})
    print(f"{'Current Price':<20} {indicators.get('current_price', 0):.5f}")
    print(f"{'EMA 20':<20} {indicators.get('ema_20', 0):.5f}")
    print(f"{'EMA 50':<20} {indicators.get('ema_50', 0):.5f}")
    print(f"{'EMA 200':<20} {indicators.get('ema_200', 0):.5f}")
    print(f"{'RSI':<20} {indicators.get('rsi', 0):.2f}")
    print(f"{'ATR':<20} {indicators.get('atr', 0):.5f}")
    
    macd = indicators.get('macd', {})
    print(f"\nMACD:")
    print(f"  Line:              {macd.get('macd', 0):.5f}")
    print(f"  Signal:            {macd.get('signal', 0):.5f}")
    print(f"  Histogram:         {macd.get('histogram', 0):.5f}")
    
    bb = indicators.get('bollinger_bands', {})
    print(f"\nBollinger Bands:")
    print(f"  Upper:             {bb.get('upper', 0):.5f}")
    print(f"  Middle:            {bb.get('middle', 0):.5f}")
    print(f"  Lower:             {bb.get('lower', 0):.5f}")
    
    print(f"\n--- Analysis ---")
    print(results.get('analysis', 'No analysis available'))
    print(f"{'='*60}\n")


async def main():
    """Main example runner"""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║          AutoGPT Trading Bot - Example Usage             ║
║                                                          ║
║  Analyzing Forex and Gold markets with technical        ║
║  indicators for scalping opportunities                   ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # Analyze multiple pairs with different market conditions
    test_scenarios = [
        ("XAUUSD", "15min", "up"),      # Gold uptrend
        ("EURUSD", "15min", "down"),    # Euro downtrend
        ("GBPUSD", "5min", "sideways"), # Pound ranging
        ("USDJPY", "30min", "up"),      # Yen uptrend
    ]
    
    print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis example uses simulated data. For real trading, integrate with:")
    print("  • MetaTrader 5 (MT5) API")
    print("  • OANDA REST API")
    print("  • Interactive Brokers API")
    print("  • yfinance for historical data\n")
    
    # Analyze each scenario
    for pair, timeframe, trend in test_scenarios:
        results = await analyze_pair(pair, timeframe, trend)
        format_signal_output(pair, results)
        
        # Small delay between analyses
        await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    print("Analysis Complete")
    print("="*60)
    print("\n⚠️  IMPORTANT REMINDERS:")
    print("  1. This is analysis only - not financial advice")
    print("  2. Always test on demo accounts first")
    print("  3. Never risk more than you can afford to lose")
    print("  4. Use proper risk management (1-2% per trade)")
    print("  5. Backtest thoroughly before live trading")
    print("\n")


def example_with_real_data():
    """
    Example of how to integrate with real data sources
    
    This is a template - you'll need to install and configure the respective APIs
    """
    
    print("\n--- Integration Examples ---\n")
    
    # Example 1: MetaTrader 5
    print("1. MetaTrader 5 Integration:")
    print("""
    import MetaTrader5 as mt5
    
    # Initialize MT5
    mt5.initialize()
    
    # Get price data
    rates = mt5.copy_rates_from_pos("XAUUSD", mt5.TIMEFRAME_M15, 0, 250)
    closes = [rate[4] for rate in rates]  # Close prices
    highs = [rate[2] for rate in rates]   # High prices
    lows = [rate[3] for rate in rates]    # Low prices
    
    # Run analysis
    # ... (use TradingBotBlock with this data)
    
    mt5.shutdown()
    """)
    
    # Example 2: OANDA
    print("\n2. OANDA API Integration:")
    print("""
    import oandapyV20
    from oandapyV20 import API
    from oandapyV20.endpoints import instruments
    
    # Initialize API
    api = API(access_token="YOUR_TOKEN")
    
    # Get candles
    params = {
        "count": 250,
        "granularity": "M15"
    }
    r = instruments.InstrumentsCandles(instrument="XAU_USD", params=params)
    api.request(r)
    
    candles = r.response['candles']
    closes = [float(c['mid']['c']) for c in candles]
    highs = [float(c['mid']['h']) for c in candles]
    lows = [float(c['mid']['l']) for c in candles]
    
    # Run analysis
    # ... (use TradingBotBlock with this data)
    """)
    
    # Example 3: yfinance for backtesting
    print("\n3. yfinance for Historical Data (Backtesting):")
    print("""
    import yfinance as yf
    
    # Download Gold data
    gold = yf.download('GC=F', period='1mo', interval='15m')
    
    closes = gold['Close'].tolist()
    highs = gold['High'].tolist()
    lows = gold['Low'].tolist()
    
    # Run analysis
    # ... (use TradingBotBlock with this data)
    """)


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" Running Trading Bot Example")
    print("="*60)
    
    # Run async analysis
    asyncio.run(main())
    
    # Show integration examples
    example_with_real_data()
    
    print("\n" + "="*60)
    print(" Example execution completed!")
    print("="*60 + "\n")
