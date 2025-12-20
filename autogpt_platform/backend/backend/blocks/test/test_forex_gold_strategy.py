"""
Tests for the Forex and Gold Strategy Block
"""

import pytest

from backend.blocks.forex_gold_strategy_block import (
    ForexGoldStrategyBlock,
    MarketType,
    TimeFrame,
    SignalType,
)


@pytest.fixture
def forex_strategy_block():
    """Create a forex strategy block instance"""
    return ForexGoldStrategyBlock()


@pytest.fixture
def sample_price_data():
    """Sample price data for testing"""
    return [
        {"open": 1.1000, "high": 1.1050, "low": 1.0950, "close": 1.1020, "volume": 1000},
        {"open": 1.1020, "high": 1.1070, "low": 1.1000, "close": 1.1060, "volume": 1100},
        {"open": 1.1060, "high": 1.1080, "low": 1.1040, "close": 1.1070, "volume": 1050},
        {"open": 1.1070, "high": 1.1100, "low": 1.1050, "close": 1.1090, "volume": 1200},
        {"open": 1.1090, "high": 1.1120, "low": 1.1080, "close": 1.1110, "volume": 1150},
        {"open": 1.1110, "high": 1.1140, "low": 1.1100, "close": 1.1130, "volume": 1300},
        {"open": 1.1130, "high": 1.1150, "low": 1.1120, "close": 1.1140, "volume": 1250},
        {"open": 1.1140, "high": 1.1160, "low": 1.1130, "close": 1.1150, "volume": 1100},
        {"open": 1.1150, "high": 1.1170, "low": 1.1140, "close": 1.1160, "volume": 1050},
        {"open": 1.1160, "high": 1.1180, "low": 1.1150, "close": 1.1170, "volume": 1200},
        {"open": 1.1170, "high": 1.1190, "low": 1.1160, "close": 1.1180, "volume": 1150},
        {"open": 1.1180, "high": 1.1200, "low": 1.1170, "close": 1.1190, "volume": 1300},
        {"open": 1.1190, "high": 1.1210, "low": 1.1180, "close": 1.1200, "volume": 1250},
        {"open": 1.1200, "high": 1.1220, "low": 1.1190, "close": 1.1210, "volume": 1100},
        {"open": 1.1210, "high": 1.1230, "low": 1.1200, "close": 1.1220, "volume": 1050},
        {"open": 1.1220, "high": 1.1240, "low": 1.1210, "close": 1.1230, "volume": 1200},
        {"open": 1.1230, "high": 1.1250, "low": 1.1220, "close": 1.1240, "volume": 1150},
        {"open": 1.1240, "high": 1.1260, "low": 1.1230, "close": 1.1250, "volume": 1300},
        {"open": 1.1250, "high": 1.1270, "low": 1.1240, "close": 1.1260, "volume": 1250},
        {"open": 1.1260, "high": 1.1280, "low": 1.1250, "close": 1.1270, "volume": 1100},
    ]


@pytest.mark.asyncio
async def test_forex_strategy_block_basic(forex_strategy_block, sample_price_data):
    """Test basic functionality of forex strategy block"""
    input_data = ForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=sample_price_data,
        confidence_threshold=0.6,
    )

    outputs = {}
    async for output_name, output_value in forex_strategy_block.run(
        input_data=input_data
    ):
        outputs[output_name] = output_value

    # Check that we got the expected outputs
    assert "signal" in outputs
    assert outputs["signal"] in [
        SignalType.BUY.value,
        SignalType.SELL.value,
        SignalType.HOLD.value,
    ]
    assert "confidence" in outputs
    assert 0.0 <= outputs["confidence"] <= 1.0
    assert "technical_analysis" in outputs
    assert "fundamental_analysis" in outputs
    assert "strategy_explanation" in outputs


@pytest.mark.asyncio
async def test_forex_strategy_block_insufficient_data(forex_strategy_block):
    """Test handling of insufficient price data"""
    input_data = ForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=[{"open": 1.1000, "high": 1.1050, "low": 1.0950, "close": 1.1020, "volume": 1000}],
        confidence_threshold=0.6,
    )

    outputs = {}
    async for output_name, output_value in forex_strategy_block.run(
        input_data=input_data
    ):
        outputs[output_name] = output_value

    assert "error" in outputs
    assert outputs["signal"] == SignalType.HOLD.value
    assert outputs["confidence"] == 0.0


@pytest.mark.asyncio
async def test_rsi_calculation(forex_strategy_block):
    """Test RSI calculation"""
    prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 104.0, 103.0, 102.0, 101.0,
              100.0, 99.0, 98.0, 97.0, 96.0, 95.0, 96.0, 97.0, 98.0, 99.0]
    rsi = forex_strategy_block.calculate_rsi(prices, period=14)

    # RSI should be between 0 and 100
    assert 0.0 <= rsi <= 100.0


@pytest.mark.asyncio
async def test_macd_calculation(forex_strategy_block):
    """Test MACD calculation"""
    prices = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0,
              110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0,
              120.0, 121.0, 122.0, 123.0, 124.0, 125.0, 126.0, 127.0]
    macd = forex_strategy_block.calculate_macd(prices)

    assert "macd" in macd
    assert "signal" in macd
    assert "histogram" in macd


@pytest.mark.asyncio
async def test_moving_averages_calculation(forex_strategy_block):
    """Test moving averages calculation"""
    prices = [100.0 + i for i in range(60)]
    ma = forex_strategy_block.calculate_moving_averages(prices, short_period=20, long_period=50)

    assert "sma_short" in ma
    assert "sma_long" in ma
    assert "crossover" in ma
    assert ma["sma_short"] > ma["sma_long"]  # Short MA should be higher in uptrend


@pytest.mark.asyncio
async def test_bollinger_bands_calculation(forex_strategy_block):
    """Test Bollinger Bands calculation"""
    prices = [100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
              95.0, 106.0, 94.0, 107.0, 93.0, 108.0, 92.0, 109.0, 91.0, 110.0,
              90.0, 111.0]
    bb = forex_strategy_block.calculate_bollinger_bands(prices, period=20, std_dev=2.0)

    assert "upper" in bb
    assert "middle" in bb
    assert "lower" in bb
    assert bb["upper"] > bb["middle"] > bb["lower"]


@pytest.mark.asyncio
async def test_atr_calculation(forex_strategy_block, sample_price_data):
    """Test ATR calculation"""
    atr = forex_strategy_block.calculate_atr(sample_price_data, period=14)

    assert isinstance(atr, float)
    assert atr >= 0.0


@pytest.mark.asyncio
async def test_stochastic_calculation(forex_strategy_block, sample_price_data):
    """Test Stochastic Oscillator calculation"""
    stoch = forex_strategy_block.calculate_stochastic(sample_price_data, k_period=14, d_period=3)

    assert "k" in stoch
    assert "d" in stoch
    assert 0.0 <= stoch["k"] <= 100.0
    assert 0.0 <= stoch["d"] <= 100.0


@pytest.mark.asyncio
async def test_fundamental_analysis(forex_strategy_block):
    """Test fundamental analysis"""
    economic_events = [
        {"name": "Interest Rate Decision", "impact": "high"},
        {"name": "GDP Release", "impact": "high"},
        {"name": "Retail Sales", "impact": "medium"},
    ]
    news_sentiment = "positive"

    analysis = forex_strategy_block.analyze_fundamental_data(economic_events, news_sentiment)

    assert "high_impact_events" in analysis
    assert analysis["high_impact_events"] == 2
    assert "medium_impact_events" in analysis
    assert analysis["medium_impact_events"] == 1
    assert "sentiment_score" in analysis
    assert analysis["sentiment_score"] > 0  # Positive sentiment
    assert "fundamental_bias" in analysis
    assert analysis["fundamental_bias"] == "bullish"


@pytest.mark.asyncio
async def test_gold_market_analysis(forex_strategy_block, sample_price_data):
    """Test analysis for gold market"""
    # Adjust price data for gold (XAUUSD typically trades around 2000)
    gold_price_data = [
        {
            "open": bar["open"] * 2000,
            "high": bar["high"] * 2000,
            "low": bar["low"] * 2000,
            "close": bar["close"] * 2000,
            "volume": bar["volume"],
        }
        for bar in sample_price_data
    ]

    input_data = ForexGoldStrategyBlock.Input(
        market_type=MarketType.GOLD,
        symbol="XAUUSD",
        timeframe=TimeFrame.H4,
        price_data=gold_price_data,
        confidence_threshold=0.6,
    )

    outputs = {}
    async for output_name, output_value in forex_strategy_block.run(
        input_data=input_data
    ):
        outputs[output_name] = output_value

    assert "signal" in outputs
    assert outputs["signal"] in [
        SignalType.BUY.value,
        SignalType.SELL.value,
        SignalType.HOLD.value,
    ]


@pytest.mark.asyncio
async def test_with_fundamental_analysis(forex_strategy_block, sample_price_data):
    """Test strategy with fundamental analysis enabled"""
    input_data = ForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=sample_price_data,
        use_fundamental_analysis=True,
        economic_events=[
            {"name": "NFP", "impact": "high"},
        ],
        news_sentiment="positive",
        confidence_threshold=0.5,
    )

    outputs = {}
    async for output_name, output_value in forex_strategy_block.run(
        input_data=input_data
    ):
        outputs[output_name] = output_value

    assert "fundamental_analysis" in outputs
    assert outputs["fundamental_analysis"]["high_impact_events"] == 1


@pytest.mark.asyncio
async def test_risk_management_levels(forex_strategy_block, sample_price_data):
    """Test that stop loss and take profit levels are calculated"""
    input_data = ForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=sample_price_data,
        confidence_threshold=0.5,
        risk_reward_ratio=2.0,
    )

    outputs = {}
    async for output_name, output_value in forex_strategy_block.run(
        input_data=input_data
    ):
        outputs[output_name] = output_value

    # If a signal is generated (not HOLD), check that risk management levels exist
    if outputs["signal"] != SignalType.HOLD.value:
        assert outputs["entry_price"] is not None
        assert outputs["stop_loss"] is not None
        assert outputs["take_profit"] is not None

        # Verify risk-reward ratio is approximately correct
        entry = outputs["entry_price"]
        sl = outputs["stop_loss"]
        tp = outputs["take_profit"]

        if outputs["signal"] == SignalType.BUY.value:
            risk = entry - sl
            reward = tp - entry
            assert reward / risk >= 1.5  # Should be close to risk_reward_ratio
        else:  # SELL
            risk = sl - entry
            reward = entry - tp
            assert reward / risk >= 1.5
