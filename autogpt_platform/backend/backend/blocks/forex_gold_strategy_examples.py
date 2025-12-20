"""
Example usage of the Forex and Gold Strategy Block

This script demonstrates how to use the forex_gold_strategy_block
to analyze trading opportunities in forex and gold markets.
"""

# Example 1: Basic Forex Analysis (EURUSD)
forex_example_input = {
    "market_type": "Forex",
    "symbol": "EURUSD",
    "timeframe": "1 Hour",
    "price_data": [
        {"open": 1.0800, "high": 1.0850, "low": 1.0750, "close": 1.0820, "volume": 1000},
        {"open": 1.0820, "high": 1.0870, "low": 1.0800, "close": 1.0860, "volume": 1100},
        {"open": 1.0860, "high": 1.0880, "low": 1.0840, "close": 1.0870, "volume": 1050},
        {"open": 1.0870, "high": 1.0900, "low": 1.0850, "close": 1.0890, "volume": 1200},
        {"open": 1.0890, "high": 1.0920, "low": 1.0880, "close": 1.0910, "volume": 1150},
        {"open": 1.0910, "high": 1.0940, "low": 1.0900, "close": 1.0930, "volume": 1300},
        {"open": 1.0930, "high": 1.0950, "low": 1.0920, "close": 1.0940, "volume": 1250},
        {"open": 1.0940, "high": 1.0960, "low": 1.0930, "close": 1.0950, "volume": 1100},
        {"open": 1.0950, "high": 1.0970, "low": 1.0940, "close": 1.0960, "volume": 1050},
        {"open": 1.0960, "high": 1.0980, "low": 1.0950, "close": 1.0970, "volume": 1200},
        {"open": 1.0970, "high": 1.0990, "low": 1.0960, "close": 1.0980, "volume": 1150},
        {"open": 1.0980, "high": 1.1000, "low": 1.0970, "close": 1.0990, "volume": 1300},
        {"open": 1.0990, "high": 1.1010, "low": 1.0980, "close": 1.1000, "volume": 1250},
        {"open": 1.1000, "high": 1.1020, "low": 1.0990, "close": 1.1010, "volume": 1100},
        {"open": 1.1010, "high": 1.1030, "low": 1.1000, "close": 1.1020, "volume": 1050},
        {"open": 1.1020, "high": 1.1040, "low": 1.1010, "close": 1.1030, "volume": 1200},
        {"open": 1.1030, "high": 1.1050, "low": 1.1020, "close": 1.1040, "volume": 1150},
        {"open": 1.1040, "high": 1.1060, "low": 1.1030, "close": 1.1050, "volume": 1300},
        {"open": 1.1050, "high": 1.1070, "low": 1.1040, "close": 1.1060, "volume": 1250},
        {"open": 1.1060, "high": 1.1080, "low": 1.1050, "close": 1.1070, "volume": 1100},
    ],
    "confidence_threshold": 0.6,
    "risk_reward_ratio": 2.0,
}

# Example 2: Gold Analysis with Fundamental Data (XAUUSD)
gold_example_input = {
    "market_type": "Gold",
    "symbol": "XAUUSD",
    "timeframe": "4 Hours",
    "price_data": [
        {"open": 2000.00, "high": 2005.00, "low": 1995.00, "close": 2002.00, "volume": 5000},
        {"open": 2002.00, "high": 2008.00, "low": 1998.00, "close": 2006.00, "volume": 5500},
        {"open": 2006.00, "high": 2010.00, "low": 2003.00, "close": 2008.00, "volume": 5200},
        {"open": 2008.00, "high": 2015.00, "low": 2005.00, "close": 2012.00, "volume": 6000},
        {"open": 2012.00, "high": 2018.00, "low": 2010.00, "close": 2016.00, "volume": 5800},
        {"open": 2016.00, "high": 2022.00, "low": 2014.00, "close": 2020.00, "volume": 6500},
        {"open": 2020.00, "high": 2025.00, "low": 2018.00, "close": 2023.00, "volume": 6300},
        {"open": 2023.00, "high": 2028.00, "low": 2021.00, "close": 2026.00, "volume": 5900},
        {"open": 2026.00, "high": 2030.00, "low": 2024.00, "close": 2028.00, "volume": 5500},
        {"open": 2028.00, "high": 2032.00, "low": 2026.00, "close": 2030.00, "volume": 6000},
        {"open": 2030.00, "high": 2035.00, "low": 2028.00, "close": 2033.00, "volume": 5800},
        {"open": 2033.00, "high": 2038.00, "low": 2031.00, "close": 2036.00, "volume": 6500},
        {"open": 2036.00, "high": 2040.00, "low": 2034.00, "close": 2038.00, "volume": 6200},
        {"open": 2038.00, "high": 2042.00, "low": 2036.00, "close": 2040.00, "volume": 5800},
        {"open": 2040.00, "high": 2044.00, "low": 2038.00, "close": 2042.00, "volume": 5500},
        {"open": 2042.00, "high": 2046.00, "low": 2040.00, "close": 2044.00, "volume": 6000},
        {"open": 2044.00, "high": 2048.00, "low": 2042.00, "close": 2046.00, "volume": 5800},
        {"open": 2046.00, "high": 2050.00, "low": 2044.00, "close": 2048.00, "volume": 6500},
        {"open": 2048.00, "high": 2052.00, "low": 2046.00, "close": 2050.00, "volume": 6200},
        {"open": 2050.00, "high": 2054.00, "low": 2048.00, "close": 2052.00, "volume": 5900},
    ],
    "use_fundamental_analysis": True,
    "economic_events": [
        {"name": "Federal Reserve Interest Rate Decision", "impact": "high"},
        {"name": "US Inflation Data (CPI)", "impact": "high"},
    ],
    "news_sentiment": "positive",  # Bullish for gold
    "confidence_threshold": 0.65,
    "risk_reward_ratio": 2.5,
}

# Example 3: Advanced Forex Strategy with Custom Indicators
advanced_forex_input = {
    "market_type": "Forex",
    "symbol": "GBPUSD",
    "timeframe": "15 Minutes",
    "price_data": [
        # Add 30+ bars of price data for more accurate indicators
        {"open": 1.2500 + i*0.0001, "high": 1.2510 + i*0.0001, 
         "low": 1.2490 + i*0.0001, "close": 1.2505 + i*0.0001, "volume": 1000}
        for i in range(30)
    ],
    # Enable all technical indicators
    "use_rsi": True,
    "rsi_period": 14,
    "rsi_oversold": 30.0,
    "rsi_overbought": 70.0,
    "use_macd": True,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "use_moving_averages": True,
    "ma_short_period": 20,
    "ma_long_period": 50,
    "use_bollinger_bands": True,
    "bb_period": 20,
    "bb_std_dev": 2.0,
    "use_atr": True,
    "atr_period": 14,
    "use_stochastic": True,
    "stoch_k_period": 14,
    "stoch_d_period": 3,
    # Fundamental analysis
    "use_fundamental_analysis": True,
    "economic_events": [
        {"name": "UK GDP", "impact": "high"},
        {"name": "US Employment Data", "impact": "high"},
    ],
    "news_sentiment": "neutral",
    "confidence_threshold": 0.6,
    "risk_reward_ratio": 2.0,
}

# Example 4: Conservative Gold Strategy (Higher Confidence)
conservative_gold_input = {
    "market_type": "Gold",
    "symbol": "XAUUSD",
    "timeframe": "1 Day",
    "price_data": [
        {"open": 2000 + i*5, "high": 2010 + i*5, 
         "low": 1990 + i*5, "close": 2005 + i*5, "volume": 10000}
        for i in range(50)  # 50 days of data
    ],
    "confidence_threshold": 0.75,  # Higher threshold for conservative approach
    "risk_reward_ratio": 3.0,      # Better risk-reward ratio
}

# Example Output Structure
example_output = {
    "signal": "BUY",  # or "SELL" or "HOLD"
    "confidence": 0.72,  # 72% confidence
    "entry_price": 1.1070,
    "stop_loss": 1.1050,   # 20 pips below entry
    "take_profit": 1.1110, # 40 pips above entry (2:1 ratio)
    "technical_analysis": {
        "rsi": 35.2,  # Oversold, bullish signal
        "macd": {
            "macd": 0.0005,
            "signal": 0.0003,
            "histogram": 0.0002  # Positive, bullish
        },
        "moving_averages": {
            "sma_short": 1.1065,
            "sma_long": 1.1050,
            "crossover": 0.0015  # Short MA above Long MA, bullish
        },
        "bollinger_bands": {
            "upper": 1.1100,
            "middle": 1.1070,
            "lower": 1.1040
        },
        "atr": 0.0020,
        "stochastic": {
            "k": 25.5,  # Oversold
            "d": 28.0
        }
    },
    "fundamental_analysis": {
        "high_impact_events": 2,
        "medium_impact_events": 0,
        "sentiment_score": 0.3,
        "fundamental_bias": "bullish"
    },
    "strategy_explanation": "Signal: BUY with 72.0% confidence | Technical score: 0.45, Fundamental score: 0.30 | RSI: 35.20 | MACD Histogram: 0.0002 | MA Crossover: Short MA 1.1065 vs Long MA 1.1050"
}

# How to use this in AutoGPT Platform:
# 
# 1. Add the "Forex Gold Strategy" block to your workflow
# 2. Connect a data source block to provide price_data
# 3. Configure the parameters based on your trading style
# 4. Connect the output to decision/trading blocks
# 5. Add notification blocks for alerts
#
# Example workflow:
# [Price Data API] → [Forex Gold Strategy] → [Decision Block] → [Trading Executor]
#                                          ↓
#                                   [Notification]

print("Forex and Gold Strategy Block - Example Configurations")
print("=" * 60)
print("\nExample 1: Basic Forex Analysis")
print(f"Symbol: {forex_example_input['symbol']}")
print(f"Timeframe: {forex_example_input['timeframe']}")
print(f"Confidence Threshold: {forex_example_input['confidence_threshold']}")
print("\nExample 2: Gold with Fundamental Analysis")
print(f"Symbol: {gold_example_input['symbol']}")
print(f"Economic Events: {len(gold_example_input['economic_events'])} high-impact events")
print(f"News Sentiment: {gold_example_input['news_sentiment']}")
print("\nExample 3: Advanced Multi-Indicator Strategy")
print(f"Symbol: {advanced_forex_input['symbol']}")
print(f"All indicators enabled: RSI, MACD, MA, BB, ATR, Stochastic")
print("\nExample 4: Conservative Long-Term Strategy")
print(f"Symbol: {conservative_gold_input['symbol']}")
print(f"Confidence Threshold: {conservative_gold_input['confidence_threshold']} (High)")
print(f"Risk-Reward Ratio: {conservative_gold_input['risk_reward_ratio']}:1")
