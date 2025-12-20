"""
Tests for the Advanced Forex and Gold Strategy Block
"""

import pytest

from backend.blocks.forex_gold_strategy_advanced import (
    AdvancedForexGoldStrategyBlock,
    MarketType,
    TimeFrame,
    SignalType,
    MarketStructure,
)


@pytest.fixture
def advanced_block():
    """Create an advanced strategy block instance"""
    return AdvancedForexGoldStrategyBlock()


@pytest.fixture
def comprehensive_price_data():
    """Comprehensive price data for testing"""
    # Generate realistic price data with trends, gaps, and volume
    data = []
    base_price = 1.1000
    
    for i in range(100):
        # Create some trending behavior
        trend = (i % 20) * 0.0002
        noise = ((-1) ** i) * 0.0001
        
        open_price = base_price + trend + noise
        high_price = open_price + 0.0005
        low_price = open_price - 0.0003
        close_price = open_price + ((-1) ** (i % 3)) * 0.0002
        volume = 1000 + (i * 10)
        
        data.append({
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume,
        })
        
        base_price = close_price
    
    return data


@pytest.mark.asyncio
async def test_fvg_detection(advanced_block, comprehensive_price_data):
    """Test Fair Value Gap detection"""
    # Add a clear FVG to the data
    test_data = comprehensive_price_data[:50]
    # Create a bullish FVG
    test_data.append({"open": 1.1000, "high": 1.1010, "low": 1.0990, "close": 1.1005, "volume": 1000})
    test_data.append({"open": 1.1005, "high": 1.1015, "low": 1.1000, "close": 1.1010, "volume": 1100})
    test_data.append({"open": 1.1030, "high": 1.1040, "low": 1.1025, "close": 1.1035, "volume": 1200})  # Gap up
    
    fvgs = advanced_block.detect_fvg(test_data, threshold=0.1)
    
    assert isinstance(fvgs, list)
    # Should detect at least one FVG
    assert len(fvgs) >= 1
    
    for fvg in fvgs:
        assert "type" in fvg
        assert fvg["type"] in ["bullish", "bearish"]
        assert "top" in fvg
        assert "bottom" in fvg
        assert fvg["top"] > fvg["bottom"]


@pytest.mark.asyncio
async def test_order_block_detection(advanced_block, comprehensive_price_data):
    """Test Order Block identification"""
    order_blocks = advanced_block.detect_order_blocks(comprehensive_price_data, strength_period=5)
    
    assert isinstance(order_blocks, list)
    
    for ob in order_blocks:
        assert "type" in ob
        assert ob["type"] in ["bullish", "bearish"]
        assert "top" in ob and "bottom" in ob
        assert ob["top"] >= ob["bottom"]
        assert "strength" in ob


@pytest.mark.asyncio
async def test_poi_identification(advanced_block, comprehensive_price_data):
    """Test Points of Interest identification"""
    fvgs = advanced_block.detect_fvg(comprehensive_price_data)
    order_blocks = advanced_block.detect_order_blocks(comprehensive_price_data)
    
    pois = advanced_block.identify_poi(comprehensive_price_data, fvgs, order_blocks)
    
    assert isinstance(pois, list)
    assert len(pois) <= 10  # Should return max 10
    
    for poi in pois:
        assert "type" in poi
        assert "price" in poi
        assert "importance" in poi


@pytest.mark.asyncio
async def test_pd_arrays(advanced_block, comprehensive_price_data):
    """Test Premium/Discount Arrays calculation"""
    pd_arrays = advanced_block.calculate_pd_arrays(comprehensive_price_data)
    
    assert "premium" in pd_arrays
    assert "discount" in pd_arrays
    assert "equilibrium" in pd_arrays
    assert "current_location" in pd_arrays
    assert pd_arrays["current_location"] in ["premium", "discount", "equilibrium"]
    
    assert isinstance(pd_arrays["premium"], list)
    assert isinstance(pd_arrays["discount"], list)


@pytest.mark.asyncio
async def test_liquidity_zones(advanced_block, comprehensive_price_data):
    """Test liquidity zone detection"""
    liquidity_zones = advanced_block.detect_liquidity_zones(comprehensive_price_data)
    
    assert isinstance(liquidity_zones, list)
    
    for zone in liquidity_zones:
        assert "type" in zone
        assert zone["type"] in ["buy_side", "sell_side"]
        assert "price" in zone
        assert "swept" in zone
        assert isinstance(zone["swept"], bool)


@pytest.mark.asyncio
async def test_support_resistance(advanced_block, comprehensive_price_data):
    """Test support and resistance level calculation"""
    sr_levels = advanced_block.calculate_support_resistance(comprehensive_price_data, lookback=50)
    
    assert "support" in sr_levels
    assert "resistance" in sr_levels
    assert isinstance(sr_levels["support"], list)
    assert isinstance(sr_levels["resistance"], list)
    
    # Support levels should be sorted descending
    if len(sr_levels["support"]) > 1:
        assert sr_levels["support"][0] >= sr_levels["support"][1]


@pytest.mark.asyncio
async def test_fibonacci_levels(advanced_block, comprehensive_price_data):
    """Test Fibonacci retracement and extension levels"""
    fib_levels = advanced_block.calculate_fibonacci_levels(comprehensive_price_data, swing_period=10)
    
    assert "trend" in fib_levels
    assert fib_levels["trend"] in ["bullish", "bearish"]
    assert "retracements" in fib_levels
    assert "extensions" in fib_levels
    
    # Check key Fibonacci ratios exist
    if fib_levels["retracements"]:
        assert "0.618" in fib_levels["retracements"]
        assert "0.382" in fib_levels["retracements"]


@pytest.mark.asyncio
async def test_pivot_points_classic(advanced_block, comprehensive_price_data):
    """Test classic pivot points calculation"""
    pivots = advanced_block.calculate_pivot_points(comprehensive_price_data, pivot_type="classic")
    
    assert "pivot" in pivots
    assert "r1" in pivots and "r2" in pivots and "r3" in pivots
    assert "s1" in pivots and "s2" in pivots and "s3" in pivots
    
    # Resistance levels should be above pivot
    assert pivots["r1"] > pivots["pivot"]
    # Support levels should be below pivot
    assert pivots["s1"] < pivots["pivot"]


@pytest.mark.asyncio
async def test_pivot_points_fibonacci(advanced_block, comprehensive_price_data):
    """Test Fibonacci pivot points calculation"""
    pivots = advanced_block.calculate_pivot_points(comprehensive_price_data, pivot_type="fibonacci")
    
    assert "pivot" in pivots
    assert "r1" in pivots
    assert "s1" in pivots


@pytest.mark.asyncio
async def test_pivot_points_camarilla(advanced_block, comprehensive_price_data):
    """Test Camarilla pivot points calculation"""
    pivots = advanced_block.calculate_pivot_points(comprehensive_price_data, pivot_type="camarilla")
    
    assert "r1" in pivots and "r4" in pivots
    assert "s1" in pivots and "s4" in pivots


@pytest.mark.asyncio
async def test_volume_profile(advanced_block, comprehensive_price_data):
    """Test volume profile calculation"""
    volume_profile = advanced_block.calculate_volume_profile(comprehensive_price_data, bins=20)
    
    assert "poc" in volume_profile  # Point of Control
    assert "value_area_high" in volume_profile
    assert "value_area_low" in volume_profile
    assert "profile" in volume_profile
    
    assert volume_profile["value_area_high"] >= volume_profile["value_area_low"]
    assert isinstance(volume_profile["profile"], list)
    assert len(volume_profile["profile"]) <= 20


@pytest.mark.asyncio
async def test_order_book_analysis(advanced_block):
    """Test order book analysis"""
    order_book_data = {
        "bids": [
            [1.1000, 1000],
            [1.0999, 500],
            [1.0998, 750],
        ],
        "asks": [
            [1.1001, 800],
            [1.1002, 600],
            [1.1003, 400],
        ],
    }
    
    analysis = advanced_block.analyze_order_book(order_book_data)
    
    assert "buy_pressure" in analysis
    assert "sell_pressure" in analysis
    assert "imbalance" in analysis
    assert "dominant_side" in analysis
    
    assert 0 <= analysis["buy_pressure"] <= 1
    assert 0 <= analysis["sell_pressure"] <= 1
    assert analysis["dominant_side"] in ["buy", "sell", "neutral"]


@pytest.mark.asyncio
async def test_market_structure_analysis(advanced_block, comprehensive_price_data):
    """Test market structure analysis"""
    market_structure = advanced_block.analyze_market_structure(comprehensive_price_data)
    
    assert "structure" in market_structure
    assert market_structure["structure"] in [
        MarketStructure.BULLISH.value,
        MarketStructure.BEARISH.value,
        MarketStructure.RANGING.value,
        MarketStructure.CHOPPY.value,
    ]
    assert "higher_highs" in market_structure
    assert "lower_lows" in market_structure
    assert "choch_detected" in market_structure


@pytest.mark.asyncio
async def test_advanced_block_full_run(advanced_block, comprehensive_price_data):
    """Test complete advanced block execution"""
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=comprehensive_price_data,
        confidence_threshold=0.65,
        use_fvg=True,
        use_order_blocks=True,
        use_poi=True,
        use_pd_arrays=True,
        use_support_resistance=True,
        use_fibonacci=True,
        use_pivot_points=True,
        use_volume_profile=True,
        use_market_structure=True,
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    # Check required outputs
    assert "signal" in outputs
    assert outputs["signal"] in [
        SignalType.STRONG_BUY.value,
        SignalType.BUY.value,
        SignalType.WEAK_BUY.value,
        SignalType.HOLD.value,
        SignalType.WEAK_SELL.value,
        SignalType.SELL.value,
        SignalType.STRONG_SELL.value,
    ]
    
    assert "confidence" in outputs
    assert 0 <= outputs["confidence"] <= 1
    
    assert "market_structure" in outputs
    assert "technical_analysis" in outputs
    assert "smc_analysis" in outputs
    assert "volume_analysis" in outputs
    assert "key_levels" in outputs
    assert "strategy_explanation" in outputs
    assert "risk_assessment" in outputs


@pytest.mark.asyncio
async def test_multiple_take_profits(advanced_block, comprehensive_price_data):
    """Test that multiple take profit levels are calculated"""
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=comprehensive_price_data,
        confidence_threshold=0.5,  # Lower threshold to get a signal
        risk_reward_ratio=2.5,
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    if outputs["signal"] != SignalType.HOLD.value:
        assert "take_profit" in outputs
        assert "take_profit_2" in outputs
        assert "take_profit_3" in outputs
        
        # TP levels should be progressively further from entry
        entry = outputs["entry_price"]
        tp1 = outputs["take_profit"]
        tp2 = outputs["take_profit_2"]
        tp3 = outputs["take_profit_3"]
        
        if "BUY" in outputs["signal"]:
            assert tp3 > tp2 > tp1 > entry
        else:  # SELL
            assert tp3 < tp2 < tp1 < entry


@pytest.mark.asyncio
async def test_insufficient_data_handling(advanced_block):
    """Test handling of insufficient data"""
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=[
            {"open": 1.1000, "high": 1.1010, "low": 1.0990, "close": 1.1005, "volume": 1000},
        ],
        confidence_threshold=0.65,
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    assert "error" in outputs
    assert outputs["signal"] == SignalType.HOLD.value
    assert outputs["confidence"] == 0.0


@pytest.mark.asyncio
async def test_crypto_market_support(advanced_block, comprehensive_price_data):
    """Test that crypto market type is supported"""
    # Scale prices for crypto (e.g., Bitcoin)
    crypto_data = [
        {
            "open": bar["open"] * 50000,
            "high": bar["high"] * 50000,
            "low": bar["low"] * 50000,
            "close": bar["close"] * 50000,
            "volume": bar["volume"],
        }
        for bar in comprehensive_price_data
    ]
    
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.CRYPTO,
        symbol="BTCUSD",
        timeframe=TimeFrame.H4,
        price_data=crypto_data,
        confidence_threshold=0.65,
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    assert "signal" in outputs
    assert outputs["confidence"] >= 0


@pytest.mark.asyncio
async def test_risk_assessment(advanced_block, comprehensive_price_data):
    """Test risk assessment output"""
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=comprehensive_price_data,
        confidence_threshold=0.65,
        use_fundamental_analysis=True,
        economic_events=[
            {"name": "NFP", "impact": "high"},
            {"name": "GDP", "impact": "high"},
        ],
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    assert "risk_assessment" in outputs
    risk = outputs["risk_assessment"]
    
    assert "risk_level" in risk
    assert risk["risk_level"] in ["low", "medium", "high", "unknown"]
    assert "risk_factors" in risk
    assert isinstance(risk["risk_factors"], list)


@pytest.mark.asyncio
async def test_all_indicators_disabled(advanced_block, comprehensive_price_data):
    """Test behavior when all indicators are disabled"""
    input_data = AdvancedForexGoldStrategyBlock.Input(
        market_type=MarketType.FOREX,
        symbol="EURUSD",
        timeframe=TimeFrame.H1,
        price_data=comprehensive_price_data,
        confidence_threshold=0.65,
        # Disable all indicators
        use_rsi=False,
        use_macd=False,
        use_moving_averages=False,
        use_bollinger_bands=False,
        use_atr=False,
        use_stochastic=False,
        use_fvg=False,
        use_order_blocks=False,
        use_poi=False,
        use_pd_arrays=False,
        use_liquidity_zones=False,
        use_support_resistance=False,
        use_fibonacci=False,
        use_pivot_points=False,
        use_volume_profile=False,
        use_order_book=False,
        use_market_structure=False,
        use_fundamental_analysis=False,
    )
    
    outputs = {}
    async for output_name, output_value in advanced_block.run(input_data=input_data):
        outputs[output_name] = output_value
    
    # Should still produce output without errors
    assert "signal" in outputs
    # With no indicators, should return HOLD
    assert outputs["signal"] == SignalType.HOLD.value
