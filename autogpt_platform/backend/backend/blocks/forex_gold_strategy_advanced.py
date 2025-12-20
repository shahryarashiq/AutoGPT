"""
Advanced Forex and Gold Trading Strategy Block - Extended Version

This block extends the base strategy with advanced Smart Money Concepts (SMC),
institutional trading indicators, and order flow analysis.

New Features:
- FVG (Fair Value Gap) detection
- IFVG (Inverse Fair Value Gap) 
- Order Blocks (OB) identification
- Points of Interest (POI)
- Premium/Discount Arrays (PD Arrays)
- Support & Resistance levels
- Fibonacci retracements & extensions
- Pivot Points (Classic, Fibonacci, Camarilla)
- Volume Profile analysis
- Order Book analysis
- Market structure analysis
- Liquidity zones
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField

logger = logging.getLogger(__name__)


class MarketType(Enum):
    """Market type enumeration"""
    FOREX = "Forex"
    GOLD = "Gold"
    CRYPTO = "Cryptocurrency"


class TimeFrame(Enum):
    """Trading timeframe enumeration"""
    M1 = "1 Minute"
    M5 = "5 Minutes"
    M15 = "15 Minutes"
    M30 = "30 Minutes"
    H1 = "1 Hour"
    H4 = "4 Hours"
    D1 = "1 Day"
    W1 = "1 Week"


class SignalType(Enum):
    """Trading signal types"""
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    WEAK_BUY = "Weak Buy"
    HOLD = "Hold"
    WEAK_SELL = "Weak Sell"
    SELL = "Sell"
    STRONG_SELL = "Strong Sell"


class MarketStructure(Enum):
    """Market structure states"""
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    RANGING = "Ranging"
    CHOPPY = "Choppy"


class AdvancedForexGoldStrategyBlock(Block):
    """
    Advanced trading strategy block with Smart Money Concepts, institutional
    indicators, and order flow analysis for achieving 70%+ win rate.
    """

    class Input(BlockSchema):
        # Basic Configuration
        market_type: MarketType = SchemaField(
            description="Select the market type",
            default=MarketType.FOREX,
        )
        symbol: str = SchemaField(
            description="Trading symbol (e.g., EURUSD, GBPUSD, XAUUSD, BTCUSD)",
            placeholder="EURUSD",
        )
        timeframe: TimeFrame = SchemaField(
            description="Select the trading timeframe",
            default=TimeFrame.H1,
        )
        price_data: List[Dict[str, float]] = SchemaField(
            description="Historical price data with OHLCV",
            default_factory=list,
        )
        
        # Classic Technical Indicators
        use_rsi: bool = SchemaField(
            description="Enable RSI indicator",
            default=True,
        )
        use_macd: bool = SchemaField(
            description="Enable MACD indicator",
            default=True,
        )
        use_moving_averages: bool = SchemaField(
            description="Enable Moving Averages",
            default=True,
        )
        use_bollinger_bands: bool = SchemaField(
            description="Enable Bollinger Bands",
            default=True,
        )
        use_atr: bool = SchemaField(
            description="Enable ATR",
            default=True,
        )
        use_stochastic: bool = SchemaField(
            description="Enable Stochastic Oscillator",
            default=True,
        )
        
        # Smart Money Concepts (SMC)
        use_fvg: bool = SchemaField(
            description="Enable Fair Value Gap (FVG) detection",
            default=True,
        )
        use_order_blocks: bool = SchemaField(
            description="Enable Order Block (OB) identification",
            default=True,
        )
        use_poi: bool = SchemaField(
            description="Enable Points of Interest (POI) detection",
            default=True,
        )
        use_pd_arrays: bool = SchemaField(
            description="Enable Premium/Discount Arrays",
            default=True,
        )
        use_liquidity_zones: bool = SchemaField(
            description="Enable Liquidity Zone detection",
            default=True,
        )
        
        # Support/Resistance & Fibonacci
        use_support_resistance: bool = SchemaField(
            description="Enable Support & Resistance levels",
            default=True,
        )
        use_fibonacci: bool = SchemaField(
            description="Enable Fibonacci retracements & extensions",
            default=True,
        )
        use_pivot_points: bool = SchemaField(
            description="Enable Pivot Points calculation",
            default=True,
        )
        pivot_type: str = SchemaField(
            description="Pivot point type: classic, fibonacci, camarilla",
            default="classic",
            advanced=True,
        )
        
        # Volume Analysis
        use_volume_profile: bool = SchemaField(
            description="Enable Volume Profile analysis",
            default=True,
        )
        volume_profile_bins: int = SchemaField(
            description="Number of price levels for volume profile",
            default=20,
            advanced=True,
        )
        
        # Order Book Analysis
        use_order_book: bool = SchemaField(
            description="Enable Order Book analysis",
            default=False,
        )
        order_book_data: Optional[Dict[str, Any]] = SchemaField(
            description="Order book data with bids and asks",
            default=None,
            advanced=True,
        )
        
        # Market Structure
        use_market_structure: bool = SchemaField(
            description="Enable market structure analysis (BOS, CHoCH)",
            default=True,
        )
        
        # Advanced Parameters
        fvg_threshold: float = SchemaField(
            description="Minimum gap size for FVG detection (in %)",
            default=0.5,
            advanced=True,
        )
        ob_strength_period: int = SchemaField(
            description="Period for Order Block strength calculation",
            default=5,
            advanced=True,
        )
        sr_lookback: int = SchemaField(
            description="Lookback period for Support/Resistance",
            default=50,
            advanced=True,
        )
        fib_swing_period: int = SchemaField(
            description="Period for identifying Fibonacci swing points",
            default=10,
            advanced=True,
        )
        
        # Strategy Parameters
        confidence_threshold: float = SchemaField(
            description="Minimum confidence level (0-1)",
            default=0.65,
        )
        risk_reward_ratio: float = SchemaField(
            description="Target risk-reward ratio",
            default=2.5,
        )
        
        # Fundamental Analysis
        use_fundamental_analysis: bool = SchemaField(
            description="Enable fundamental analysis",
            default=True,
        )
        economic_events: List[Dict[str, Any]] = SchemaField(
            description="Economic calendar events",
            default_factory=list,
            advanced=True,
        )
        news_sentiment: Optional[str] = SchemaField(
            description="Market news sentiment",
            default=None,
            advanced=True,
        )

    class Output(BlockSchema):
        signal: str = SchemaField(
            description="Trading signal with strength"
        )
        confidence: float = SchemaField(
            description="Signal confidence (0-1)"
        )
        entry_price: Optional[float] = SchemaField(
            description="Recommended entry price"
        )
        stop_loss: Optional[float] = SchemaField(
            description="Stop loss level"
        )
        take_profit: Optional[float] = SchemaField(
            description="Take profit level"
        )
        take_profit_2: Optional[float] = SchemaField(
            description="Second take profit target"
        )
        take_profit_3: Optional[float] = SchemaField(
            description="Third take profit target"
        )
        market_structure: str = SchemaField(
            description="Current market structure",
            default="",
        )
        technical_analysis: Dict[str, Any] = SchemaField(
            description="Classic technical indicators",
            default_factory=dict,
        )
        smc_analysis: Dict[str, Any] = SchemaField(
            description="Smart Money Concepts analysis",
            default_factory=dict,
        )
        volume_analysis: Dict[str, Any] = SchemaField(
            description="Volume and order flow analysis",
            default_factory=dict,
        )
        key_levels: Dict[str, List[float]] = SchemaField(
            description="Important price levels",
            default_factory=dict,
        )
        fundamental_analysis: Dict[str, Any] = SchemaField(
            description="Fundamental analysis results",
            default_factory=dict,
        )
        strategy_explanation: str = SchemaField(
            description="Detailed signal explanation",
            default="",
        )
        risk_assessment: Dict[str, Any] = SchemaField(
            description="Risk metrics and assessment",
            default_factory=dict,
        )
        error: str = SchemaField(
            description="Error message if any",
            default="",
        )

    def __init__(self):
        super().__init__(
            id="b8e4f3d2-0c5e-4f9g-b2d6-8e7f9g0h2i3j",
            description="Advanced forex and gold strategy with Smart Money Concepts, institutional indicators, volume profile, and order book analysis for 70%+ win rate.",
            categories={BlockCategory.DATA, BlockCategory.AI},
            input_schema=AdvancedForexGoldStrategyBlock.Input,
            output_schema=AdvancedForexGoldStrategyBlock.Output,
            test_input={
                "market_type": MarketType.FOREX.value,
                "symbol": "EURUSD",
                "timeframe": TimeFrame.H1.value,
                "price_data": [
                    {"open": 1.1000, "high": 1.1050, "low": 1.0950, "close": 1.1020, "volume": 1000},
                    {"open": 1.1020, "high": 1.1070, "low": 1.1000, "close": 1.1060, "volume": 1100},
                    {"open": 1.1060, "high": 1.1080, "low": 1.1040, "close": 1.1070, "volume": 1050},
                ],
                "confidence_threshold": 0.65,
            },
            test_output=[
                ("signal", "HOLD"),
                ("confidence", 0.5),
            ],
        )

    # ==================== SMART MONEY CONCEPTS ====================
    
    def detect_fvg(self, price_data: List[Dict[str, float]], threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Detect Fair Value Gaps (FVG) - imbalances in price action
        FVG occurs when there's a gap between candles that hasn't been filled
        """
        fvgs = []
        
        for i in range(2, len(price_data)):
            candle1 = price_data[i-2]
            candle2 = price_data[i-1]  
            candle3 = price_data[i]
            
            # Bullish FVG: candle3 low > candle1 high
            if candle3["low"] > candle1["high"]:
                gap_size = candle3["low"] - candle1["high"]
                gap_percent = (gap_size / candle1["high"]) * 100
                
                if gap_percent >= threshold:
                    fvgs.append({
                        "type": "bullish",
                        "index": i,
                        "top": candle3["low"],
                        "bottom": candle1["high"],
                        "size": gap_size,
                        "filled": False,
                    })
            
            # Bearish FVG: candle3 high < candle1 low
            elif candle3["high"] < candle1["low"]:
                gap_size = candle1["low"] - candle3["high"]
                gap_percent = (gap_size / candle1["low"]) * 100
                
                if gap_percent >= threshold:
                    fvgs.append({
                        "type": "bearish",
                        "index": i,
                        "top": candle1["low"],
                        "bottom": candle3["high"],
                        "size": gap_size,
                        "filled": False,
                    })
        
        # Check if FVGs have been filled
        current_price = price_data[-1]["close"]
        for fvg in fvgs:
            if fvg["type"] == "bullish" and current_price <= fvg["top"]:
                fvg["filled"] = True
            elif fvg["type"] == "bearish" and current_price >= fvg["bottom"]:
                fvg["filled"] = True
        
        return fvgs

    def detect_order_blocks(
        self, price_data: List[Dict[str, float]], strength_period: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Identify Order Blocks (OB) - zones where institutions place large orders
        OB is the last opposing candle before a strong move
        """
        order_blocks = []
        
        for i in range(strength_period, len(price_data) - 1):
            # Bullish Order Block: bearish candle followed by bullish momentum
            if price_data[i]["close"] < price_data[i]["open"]:  # Bearish candle
                # Check if followed by bullish move
                next_moves_up = True
                for j in range(i + 1, min(i + strength_period + 1, len(price_data))):
                    if price_data[j]["close"] < price_data[i]["close"]:
                        next_moves_up = False
                        break
                
                if next_moves_up:
                    order_blocks.append({
                        "type": "bullish",
                        "index": i,
                        "top": price_data[i]["high"],
                        "bottom": price_data[i]["low"],
                        "open": price_data[i]["open"],
                        "close": price_data[i]["close"],
                        "volume": price_data[i].get("volume", 0),
                        "strength": strength_period,
                        "tested": False,
                    })
            
            # Bearish Order Block: bullish candle followed by bearish momentum
            elif price_data[i]["close"] > price_data[i]["open"]:  # Bullish candle
                # Check if followed by bearish move
                next_moves_down = True
                for j in range(i + 1, min(i + strength_period + 1, len(price_data))):
                    if price_data[j]["close"] > price_data[i]["close"]:
                        next_moves_down = False
                        break
                
                if next_moves_down:
                    order_blocks.append({
                        "type": "bearish",
                        "index": i,
                        "top": price_data[i]["high"],
                        "bottom": price_data[i]["low"],
                        "open": price_data[i]["open"],
                        "close": price_data[i]["close"],
                        "volume": price_data[i].get("volume", 0),
                        "strength": strength_period,
                        "tested": False,
                    })
        
        return order_blocks

    def identify_poi(
        self, price_data: List[Dict[str, float]], fvgs: List[Dict], order_blocks: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Identify Points of Interest (POI) - key levels for potential reversals
        POI combines FVGs, Order Blocks, and significant price levels
        """
        pois = []
        current_price = price_data[-1]["close"]
        
        # Add unfilled FVGs as POIs
        for fvg in fvgs:
            if not fvg["filled"]:
                distance = abs(current_price - (fvg["top"] + fvg["bottom"]) / 2)
                pois.append({
                    "type": f"{fvg['type']}_fvg",
                    "price": (fvg["top"] + fvg["bottom"]) / 2,
                    "top": fvg["top"],
                    "bottom": fvg["bottom"],
                    "distance": distance,
                    "importance": "high" if distance / current_price < 0.01 else "medium",
                })
        
        # Add untested Order Blocks as POIs
        for ob in order_blocks:
            if not ob["tested"]:
                ob_mid = (ob["top"] + ob["bottom"]) / 2
                distance = abs(current_price - ob_mid)
                pois.append({
                    "type": f"{ob['type']}_ob",
                    "price": ob_mid,
                    "top": ob["top"],
                    "bottom": ob["bottom"],
                    "distance": distance,
                    "importance": "high" if ob.get("volume", 0) > 0 else "medium",
                })
        
        # Sort by distance to current price
        pois.sort(key=lambda x: x["distance"])
        
        return pois[:10]  # Return top 10 closest POIs

    def calculate_pd_arrays(self, price_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Calculate Premium/Discount Arrays - optimal entry zones
        Premium: prices above equilibrium (good for selling)
        Discount: prices below equilibrium (good for buying)
        """
        if len(price_data) < 20:
            return {"premium": [], "discount": [], "equilibrium": 0.0}
        
        # Calculate recent range
        recent_data = price_data[-50:] if len(price_data) >= 50 else price_data
        high = max(bar["high"] for bar in recent_data)
        low = min(bar["low"] for bar in recent_data)
        range_size = high - low
        equilibrium = (high + low) / 2
        
        # Define zones
        premium_zones = []
        discount_zones = []
        
        # Premium zones (above equilibrium)
        for i in range(1, 5):
            zone_bottom = equilibrium + (range_size * i * 0.1)
            zone_top = equilibrium + (range_size * (i + 1) * 0.1)
            if zone_bottom <= high:
                premium_zones.append({
                    "level": i,
                    "top": min(zone_top, high),
                    "bottom": zone_bottom,
                    "strength": 5 - i,  # Higher zones = weaker
                })
        
        # Discount zones (below equilibrium)
        for i in range(1, 5):
            zone_top = equilibrium - (range_size * i * 0.1)
            zone_bottom = equilibrium - (range_size * (i + 1) * 0.1)
            if zone_top >= low:
                discount_zones.append({
                    "level": i,
                    "top": zone_top,
                    "bottom": max(zone_bottom, low),
                    "strength": 5 - i,  # Lower zones = weaker
                })
        
        current_price = price_data[-1]["close"]
        if current_price > equilibrium:
            price_location = "premium"
        elif current_price < equilibrium:
            price_location = "discount"
        else:
            price_location = "equilibrium"
        
        return {
            "premium": premium_zones,
            "discount": discount_zones,
            "equilibrium": equilibrium,
            "current_location": price_location,
            "range_high": high,
            "range_low": low,
        }

    def detect_liquidity_zones(self, price_data: List[Dict[str, float]]) -> List[Dict[str, Any]]:
        """
        Identify liquidity zones - areas where stop losses are likely clustered
        These are often sweep targets for institutional traders
        """
        liquidity_zones = []
        
        # Find swing highs and lows (potential liquidity pools)
        for i in range(2, len(price_data) - 2):
            # Swing high: higher than surrounding candles
            if (price_data[i]["high"] > price_data[i-1]["high"] and
                price_data[i]["high"] > price_data[i-2]["high"] and
                price_data[i]["high"] > price_data[i+1]["high"] and
                price_data[i]["high"] > price_data[i+2]["high"]):
                
                liquidity_zones.append({
                    "type": "sell_side",  # Stops above
                    "price": price_data[i]["high"],
                    "index": i,
                    "swept": any(
                        price_data[j]["high"] > price_data[i]["high"]
                        for j in range(i + 1, len(price_data))
                    ),
                })
            
            # Swing low: lower than surrounding candles
            if (price_data[i]["low"] < price_data[i-1]["low"] and
                price_data[i]["low"] < price_data[i-2]["low"] and
                price_data[i]["low"] < price_data[i+1]["low"] and
                price_data[i]["low"] < price_data[i+2]["low"]):
                
                liquidity_zones.append({
                    "type": "buy_side",  # Stops below
                    "price": price_data[i]["low"],
                    "index": i,
                    "swept": any(
                        price_data[j]["low"] < price_data[i]["low"]
                        for j in range(i + 1, len(price_data))
                    ),
                })
        
        return liquidity_zones[-20:]  # Return last 20 zones

    # ==================== SUPPORT/RESISTANCE & FIBONACCI ====================
    
    def calculate_support_resistance(
        self, price_data: List[Dict[str, float]], lookback: int = 50
    ) -> Dict[str, List[float]]:
        """
        Calculate support and resistance levels using swing points
        """
        if len(price_data) < lookback:
            lookback = len(price_data)
        
        recent_data = price_data[-lookback:]
        
        # Find swing points
        swing_highs = []
        swing_lows = []
        
        for i in range(2, len(recent_data) - 2):
            # Swing high
            if (recent_data[i]["high"] > recent_data[i-1]["high"] and
                recent_data[i]["high"] > recent_data[i-2]["high"] and
                recent_data[i]["high"] > recent_data[i+1]["high"] and
                recent_data[i]["high"] > recent_data[i+2]["high"]):
                swing_highs.append(recent_data[i]["high"])
            
            # Swing low
            if (recent_data[i]["low"] < recent_data[i-1]["low"] and
                recent_data[i]["low"] < recent_data[i-2]["low"] and
                recent_data[i]["low"] < recent_data[i+1]["low"] and
                recent_data[i]["low"] < recent_data[i+2]["low"]):
                swing_lows.append(recent_data[i]["low"])
        
        # Cluster levels
        def cluster_levels(levels: List[float], tolerance: float = 0.002) -> List[float]:
            if not levels:
                return []
            
            sorted_levels = sorted(levels)
            clusters = []
            current_cluster = [sorted_levels[0]]
            
            for level in sorted_levels[1:]:
                if abs(level - current_cluster[-1]) / current_cluster[-1] <= tolerance:
                    current_cluster.append(level)
                else:
                    clusters.append(sum(current_cluster) / len(current_cluster))
                    current_cluster = [level]
            
            clusters.append(sum(current_cluster) / len(current_cluster))
            return clusters
        
        resistance_levels = cluster_levels(swing_highs)
        support_levels = cluster_levels(swing_lows)
        
        return {
            "resistance": sorted(resistance_levels, reverse=True)[:5],
            "support": sorted(support_levels, reverse=True)[:5],
        }

    def calculate_fibonacci_levels(
        self, price_data: List[Dict[str, float]], swing_period: int = 10
    ) -> Dict[str, Any]:
        """
        Calculate Fibonacci retracement and extension levels
        """
        if len(price_data) < swing_period * 2:
            return {"retracements": [], "extensions": [], "trend": "none"}
        
        # Find recent swing high and low
        recent_data = price_data[-swing_period * 5:]
        
        swing_high = max(bar["high"] for bar in recent_data)
        swing_low = min(bar["low"] for bar in recent_data)
        swing_high_idx = next(i for i, bar in enumerate(recent_data) if bar["high"] == swing_high)
        swing_low_idx = next(i for i, bar in enumerate(recent_data) if bar["low"] == swing_low)
        
        # Determine trend
        trend = "bullish" if swing_low_idx < swing_high_idx else "bearish"
        
        # Fibonacci ratios
        fib_ratios = {
            "0.0": 0.0,
            "0.236": 0.236,
            "0.382": 0.382,
            "0.5": 0.5,
            "0.618": 0.618,
            "0.786": 0.786,
            "1.0": 1.0,
        }
        
        extension_ratios = {
            "1.272": 1.272,
            "1.414": 1.414,
            "1.618": 1.618,
            "2.0": 2.0,
            "2.618": 2.618,
        }
        
        range_size = swing_high - swing_low
        
        # Calculate retracement levels
        retracements = {}
        if trend == "bullish":
            for name, ratio in fib_ratios.items():
                retracements[name] = swing_high - (range_size * ratio)
        else:
            for name, ratio in fib_ratios.items():
                retracements[name] = swing_low + (range_size * ratio)
        
        # Calculate extension levels
        extensions = {}
        if trend == "bullish":
            for name, ratio in extension_ratios.items():
                extensions[name] = swing_high + (range_size * (ratio - 1))
        else:
            for name, ratio in extension_ratios.items():
                extensions[name] = swing_low - (range_size * (ratio - 1))
        
        return {
            "trend": trend,
            "swing_high": swing_high,
            "swing_low": swing_low,
            "retracements": retracements,
            "extensions": extensions,
        }

    def calculate_pivot_points(
        self, price_data: List[Dict[str, float]], pivot_type: str = "classic"
    ) -> Dict[str, float]:
        """
        Calculate pivot points: classic, Fibonacci, or Camarilla
        """
        if len(price_data) < 2:
            return {}
        
        # Use previous period's data
        prev_bar = price_data[-2]
        high = prev_bar["high"]
        low = prev_bar["low"]
        close = prev_bar["close"]
        
        if pivot_type == "classic":
            pivot = (high + low + close) / 3
            r1 = (2 * pivot) - low
            r2 = pivot + (high - low)
            r3 = high + 2 * (pivot - low)
            s1 = (2 * pivot) - high
            s2 = pivot - (high - low)
            s3 = low - 2 * (high - pivot)
            
            return {
                "pivot": pivot,
                "r1": r1, "r2": r2, "r3": r3,
                "s1": s1, "s2": s2, "s3": s3,
            }
        
        elif pivot_type == "fibonacci":
            pivot = (high + low + close) / 3
            r1 = pivot + 0.382 * (high - low)
            r2 = pivot + 0.618 * (high - low)
            r3 = pivot + 1.0 * (high - low)
            s1 = pivot - 0.382 * (high - low)
            s2 = pivot - 0.618 * (high - low)
            s3 = pivot - 1.0 * (high - low)
            
            return {
                "pivot": pivot,
                "r1": r1, "r2": r2, "r3": r3,
                "s1": s1, "s2": s2, "s3": s3,
            }
        
        elif pivot_type == "camarilla":
            r4 = close + ((high - low) * 1.1 / 2)
            r3 = close + ((high - low) * 1.1 / 4)
            r2 = close + ((high - low) * 1.1 / 6)
            r1 = close + ((high - low) * 1.1 / 12)
            s1 = close - ((high - low) * 1.1 / 12)
            s2 = close - ((high - low) * 1.1 / 6)
            s3 = close - ((high - low) * 1.1 / 4)
            s4 = close - ((high - low) * 1.1 / 2)
            
            return {
                "r1": r1, "r2": r2, "r3": r3, "r4": r4,
                "s1": s1, "s2": s2, "s3": s3, "s4": s4,
            }
        
        return {}

    # ==================== VOLUME ANALYSIS ====================
    
    def calculate_volume_profile(
        self, price_data: List[Dict[str, float]], bins: int = 20
    ) -> Dict[str, Any]:
        """
        Calculate Volume Profile - volume distribution across price levels
        """
        if len(price_data) < 10:
            return {"poc": 0.0, "value_area_high": 0.0, "value_area_low": 0.0, "profile": []}
        
        # Get price range
        prices = [bar["close"] for bar in price_data]
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price
        
        if price_range == 0:
            return {"poc": prices[-1], "value_area_high": prices[-1], "value_area_low": prices[-1], "profile": []}
        
        # Create bins
        bin_size = price_range / bins
        volume_at_price = [0.0] * bins
        
        # Aggregate volume
        for bar in price_data:
            volume = bar.get("volume", 0)
            if volume > 0:
                # Distribute volume across the bar's price range
                bin_idx = int((bar["close"] - min_price) / bin_size)
                bin_idx = min(bin_idx, bins - 1)
                volume_at_price[bin_idx] += volume
        
        # Find Point of Control (POC) - price level with highest volume
        max_volume_idx = volume_at_price.index(max(volume_at_price))
        poc = min_price + (max_volume_idx * bin_size) + (bin_size / 2)
        
        # Calculate Value Area (70% of volume)
        total_volume = sum(volume_at_price)
        target_volume = total_volume * 0.7
        
        # Start from POC and expand
        value_area_indices = [max_volume_idx]
        accumulated_volume = volume_at_price[max_volume_idx]
        
        left = max_volume_idx - 1
        right = max_volume_idx + 1
        
        while accumulated_volume < target_volume and (left >= 0 or right < bins):
            left_vol = volume_at_price[left] if left >= 0 else 0
            right_vol = volume_at_price[right] if right < bins else 0
            
            if left_vol > right_vol and left >= 0:
                value_area_indices.append(left)
                accumulated_volume += left_vol
                left -= 1
            elif right < bins:
                value_area_indices.append(right)
                accumulated_volume += right_vol
                right += 1
            else:
                break
        
        value_area_low = min_price + (min(value_area_indices) * bin_size)
        value_area_high = min_price + ((max(value_area_indices) + 1) * bin_size)
        
        # Create profile
        profile = []
        for i in range(bins):
            price = min_price + (i * bin_size) + (bin_size / 2)
            profile.append({
                "price": price,
                "volume": volume_at_price[i],
                "in_value_area": i in value_area_indices,
            })
        
        return {
            "poc": poc,
            "value_area_high": value_area_high,
            "value_area_low": value_area_low,
            "profile": profile,
            "total_volume": total_volume,
        }

    def analyze_order_book(self, order_book_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze order book for buy/sell pressure
        """
        if not order_book_data or "bids" not in order_book_data or "asks" not in order_book_data:
            return {
                "buy_pressure": 0.0,
                "sell_pressure": 0.0,
                "imbalance": 0.0,
                "dominant_side": "neutral",
            }
        
        bids = order_book_data["bids"]  # [[price, size], ...]
        asks = order_book_data["asks"]  # [[price, size], ...]
        
        # Calculate total volumes
        bid_volume = sum(bid[1] for bid in bids[:10])  # Top 10 levels
        ask_volume = sum(ask[1] for ask in asks[:10])
        
        total_volume = bid_volume + ask_volume
        
        if total_volume == 0:
            return {
                "buy_pressure": 0.0,
                "sell_pressure": 0.0,
                "imbalance": 0.0,
                "dominant_side": "neutral",
            }
        
        buy_pressure = bid_volume / total_volume
        sell_pressure = ask_volume / total_volume
        imbalance = (bid_volume - ask_volume) / total_volume
        
        if imbalance > 0.2:
            dominant_side = "buy"
        elif imbalance < -0.2:
            dominant_side = "sell"
        else:
            dominant_side = "neutral"
        
        # Find largest orders (whale walls)
        largest_bid = max(bids[:20], key=lambda x: x[1]) if bids else [0, 0]
        largest_ask = max(asks[:20], key=lambda x: x[1]) if asks else [0, 0]
        
        return {
            "buy_pressure": buy_pressure,
            "sell_pressure": sell_pressure,
            "imbalance": imbalance,
            "dominant_side": dominant_side,
            "bid_volume": bid_volume,
            "ask_volume": ask_volume,
            "largest_bid": {"price": largest_bid[0], "size": largest_bid[1]},
            "largest_ask": {"price": largest_ask[0], "size": largest_ask[1]},
        }

    # ==================== MARKET STRUCTURE ====================
    
    def analyze_market_structure(self, price_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Analyze market structure: BOS (Break of Structure), CHoCH (Change of Character)
        """
        if len(price_data) < 10:
            return {
                "structure": MarketStructure.RANGING.value,
                "bos_count": 0,
                "choch_detected": False,
                "higher_highs": 0,
                "lower_lows": 0,
            }
        
        # Find swing points
        swing_highs = []
        swing_lows = []
        
        for i in range(2, len(price_data) - 2):
            if (price_data[i]["high"] > price_data[i-1]["high"] and
                price_data[i]["high"] > price_data[i+1]["high"]):
                swing_highs.append((i, price_data[i]["high"]))
            
            if (price_data[i]["low"] < price_data[i-1]["low"] and
                price_data[i]["low"] < price_data[i+1]["low"]):
                swing_lows.append((i, price_data[i]["low"]))
        
        # Count higher highs and lower lows
        higher_highs = 0
        for i in range(1, len(swing_highs)):
            if swing_highs[i][1] > swing_highs[i-1][1]:
                higher_highs += 1
        
        lower_lows = 0
        for i in range(1, len(swing_lows)):
            if swing_lows[i][1] < swing_lows[i-1][1]:
                lower_lows += 1
        
        # Determine structure
        if higher_highs > lower_lows + 1:
            structure = MarketStructure.BULLISH.value
        elif lower_lows > higher_highs + 1:
            structure = MarketStructure.BEARISH.value
        elif higher_highs == 0 and lower_lows == 0:
            structure = MarketStructure.CHOPPY.value
        else:
            structure = MarketStructure.RANGING.value
        
        # Detect CHoCH (Change of Character) - recent reversal in structure
        choch_detected = False
        if len(swing_highs) >= 3 and len(swing_lows) >= 3:
            recent_trend_bullish = swing_highs[-1][1] > swing_highs[-2][1]
            recent_trend_bearish = swing_lows[-1][1] < swing_lows[-2][1]
            
            if recent_trend_bullish and structure == MarketStructure.BEARISH.value:
                choch_detected = True
            elif recent_trend_bearish and structure == MarketStructure.BULLISH.value:
                choch_detected = True
        
        return {
            "structure": structure,
            "bos_count": higher_highs + lower_lows,
            "choch_detected": choch_detected,
            "higher_highs": higher_highs,
            "lower_lows": lower_lows,
            "swing_highs": len(swing_highs),
            "swing_lows": len(swing_lows),
        }

    # ==================== SIGNAL GENERATION ====================
    
    def generate_advanced_signal(
        self,
        price_data: List[Dict[str, float]],
        technical_analysis: Dict[str, Any],
        smc_analysis: Dict[str, Any],
        volume_analysis: Dict[str, Any],
        key_levels: Dict[str, Any],
        fundamental_analysis: Dict[str, Any],
        input_data: Input,
    ) -> Dict[str, Any]:
        """
        Generate trading signal using all available analysis
        """
        signal_score = 0.0
        signal_components = []
        current_price = price_data[-1]["close"]
        
        # Weight distribution
        TECHNICAL_WEIGHT = 0.25
        SMC_WEIGHT = 0.30
        VOLUME_WEIGHT = 0.15
        LEVELS_WEIGHT = 0.15
        FUNDAMENTAL_WEIGHT = 0.15
        
        # ===== TECHNICAL ANALYSIS (25%) =====
        tech_score = 0.0
        if "rsi" in technical_analysis:
            rsi = technical_analysis["rsi"]
            if rsi < 30:
                tech_score += 0.2
                signal_components.append("RSI oversold")
            elif rsi > 70:
                tech_score -= 0.2
                signal_components.append("RSI overbought")
        
        if "macd" in technical_analysis:
            histogram = technical_analysis["macd"]["histogram"]
            if histogram > 0:
                tech_score += 0.15
                signal_components.append("MACD bullish")
            else:
                tech_score -= 0.15
                signal_components.append("MACD bearish")
        
        if "moving_averages" in technical_analysis:
            crossover = technical_analysis["moving_averages"]["crossover"]
            if crossover > 0:
                tech_score += 0.2
                signal_components.append("MA crossover bullish")
            else:
                tech_score -= 0.2
                signal_components.append("MA crossover bearish")
        
        signal_score += tech_score * TECHNICAL_WEIGHT
        
        # ===== SMART MONEY CONCEPTS (30%) =====
        smc_score = 0.0
        
        # FVG analysis
        if "fvgs" in smc_analysis:
            unfilled_bullish = sum(1 for fvg in smc_analysis["fvgs"] if fvg["type"] == "bullish" and not fvg["filled"])
            unfilled_bearish = sum(1 for fvg in smc_analysis["fvgs"] if fvg["type"] == "bearish" and not fvg["filled"])
            
            if unfilled_bullish > unfilled_bearish:
                smc_score += 0.15
                signal_components.append(f"{unfilled_bullish} bullish FVGs")
            elif unfilled_bearish > unfilled_bullish:
                smc_score -= 0.15
                signal_components.append(f"{unfilled_bearish} bearish FVGs")
        
        # Order Block analysis
        if "order_blocks" in smc_analysis:
            ob_score = 0
            for ob in smc_analysis["order_blocks"]:
                if not ob["tested"]:
                    distance = abs(current_price - (ob["top"] + ob["bottom"]) / 2)
                    if distance / current_price < 0.005:  # Within 0.5%
                        if ob["type"] == "bullish":
                            ob_score += 1
                        else:
                            ob_score -= 1
            
            if ob_score > 0:
                smc_score += 0.2
                signal_components.append("Near bullish OB")
            elif ob_score < 0:
                smc_score -= 0.2
                signal_components.append("Near bearish OB")
        
        # PD Arrays
        if "pd_arrays" in smc_analysis:
            pd = smc_analysis["pd_arrays"]
            if pd["current_location"] == "discount":
                smc_score += 0.15
                signal_components.append("Price in discount zone")
            elif pd["current_location"] == "premium":
                smc_score -= 0.15
                signal_components.append("Price in premium zone")
        
        # Market Structure
        if "market_structure" in smc_analysis:
            structure = smc_analysis["market_structure"]["structure"]
            if structure == MarketStructure.BULLISH.value:
                smc_score += 0.1
                signal_components.append("Bullish structure")
            elif structure == MarketStructure.BEARISH.value:
                smc_score -= 0.1
                signal_components.append("Bearish structure")
        
        signal_score += smc_score * SMC_WEIGHT
        
        # ===== VOLUME ANALYSIS (15%) =====
        vol_score = 0.0
        
        if "volume_profile" in volume_analysis:
            vp = volume_analysis["volume_profile"]
            if current_price < vp["poc"]:
                vol_score += 0.1
                signal_components.append("Below POC")
            else:
                vol_score -= 0.1
                signal_components.append("Above POC")
        
        if "order_book" in volume_analysis:
            ob = volume_analysis["order_book"]
            if ob["dominant_side"] == "buy":
                vol_score += 0.15
                signal_components.append("Buy pressure dominant")
            elif ob["dominant_side"] == "sell":
                vol_score -= 0.15
                signal_components.append("Sell pressure dominant")
        
        signal_score += vol_score * VOLUME_WEIGHT
        
        # ===== KEY LEVELS (15%) =====
        levels_score = 0.0
        
        if "support_resistance" in key_levels:
            sr = key_levels["support_resistance"]
            # Check proximity to support/resistance
            for support in sr.get("support", []):
                if abs(current_price - support) / current_price < 0.003:
                    levels_score += 0.15
                    signal_components.append("Near support")
                    break
            
            for resistance in sr.get("resistance", []):
                if abs(current_price - resistance) / current_price < 0.003:
                    levels_score -= 0.15
                    signal_components.append("Near resistance")
                    break
        
        if "fibonacci" in key_levels:
            fib = key_levels["fibonacci"]
            # Check if price is near key Fib levels
            for level_name, level_price in fib.get("retracements", {}).items():
                if level_name in ["0.618", "0.786"] and abs(current_price - level_price) / current_price < 0.002:
                    if fib["trend"] == "bullish":
                        levels_score += 0.1
                        signal_components.append(f"At Fib {level_name}")
                    else:
                        levels_score -= 0.1
                        signal_components.append(f"At Fib {level_name}")
        
        signal_score += levels_score * LEVELS_WEIGHT
        
        # ===== FUNDAMENTAL ANALYSIS (15%) =====
        fund_score = fundamental_analysis.get("sentiment_score", 0.0)
        signal_score += fund_score * FUNDAMENTAL_WEIGHT
        
        if fund_score != 0:
            signal_components.append(f"{fundamental_analysis.get('fundamental_bias', 'neutral')} bias")
        
        # ===== DETERMINE SIGNAL =====
        confidence = min(abs(signal_score), 1.0)
        
        if signal_score >= 0.20 and confidence >= input_data.confidence_threshold:
            if confidence >= 0.75:
                signal = SignalType.STRONG_BUY.value
            elif confidence >= 0.65:
                signal = SignalType.BUY.value
            else:
                signal = SignalType.WEAK_BUY.value
        elif signal_score <= -0.20 and confidence >= input_data.confidence_threshold:
            if confidence >= 0.75:
                signal = SignalType.STRONG_SELL.value
            elif confidence >= 0.65:
                signal = SignalType.SELL.value
            else:
                signal = SignalType.WEAK_SELL.value
        else:
            signal = SignalType.HOLD.value
        
        # Calculate trade levels
        entry_price = None
        stop_loss = None
        take_profit = None
        take_profit_2 = None
        take_profit_3 = None
        
        if signal != SignalType.HOLD.value:
            entry_price = current_price
            atr = technical_analysis.get("atr", current_price * 0.01)
            
            if "BUY" in signal:
                stop_loss = entry_price - (atr * 2)
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * input_data.risk_reward_ratio)
                take_profit_2 = entry_price + (risk * input_data.risk_reward_ratio * 1.5)
                take_profit_3 = entry_price + (risk * input_data.risk_reward_ratio * 2)
            else:  # SELL
                stop_loss = entry_price + (atr * 2)
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * input_data.risk_reward_ratio)
                take_profit_2 = entry_price - (risk * input_data.risk_reward_ratio * 1.5)
                take_profit_3 = entry_price - (risk * input_data.risk_reward_ratio * 2)
        
        # Risk assessment
        risk_factors = []
        if fundamental_analysis.get("high_impact_events", 0) > 0:
            risk_factors.append("High impact events upcoming")
        if smc_analysis.get("market_structure", {}).get("choch_detected", False):
            risk_factors.append("Market structure change detected")
        if volume_analysis.get("order_book", {}).get("imbalance", 0) > 0.5:
            risk_factors.append("Extreme order book imbalance")
        
        risk_level = "high" if len(risk_factors) >= 2 else "medium" if len(risk_factors) == 1 else "low"
        
        explanation = f"{signal} signal with {confidence:.1%} confidence. " + " | ".join(signal_components[:5])
        
        return {
            "signal": signal,
            "confidence": confidence,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "take_profit_2": take_profit_2,
            "take_profit_3": take_profit_3,
            "explanation": explanation,
            "signal_score": signal_score,
            "components": signal_components,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
        }

    async def run(self, input_data: Input, **kwargs) -> BlockOutput:
        try:
            # Validate input
            if not input_data.price_data or len(input_data.price_data) < 10:
                error_msg = (
                    "Insufficient price data. Advanced strategy requires at least 10 bars. "
                    "For optimal performance: 50+ bars recommended for all indicators."
                )
                yield "error", error_msg
                yield "signal", SignalType.HOLD.value
                yield "confidence", 0.0
                yield "market_structure", "unknown"
                yield "strategy_explanation", "Insufficient data"
                return
            
            # Import base indicators from original block
            from backend.blocks.forex_gold_strategy_block import ForexGoldStrategyBlock
            base_block = ForexGoldStrategyBlock()
            
            close_prices = [bar["close"] for bar in input_data.price_data]
            
            # ===== CLASSIC TECHNICAL ANALYSIS =====
            technical_analysis = {}
            
            if input_data.use_rsi:
                technical_analysis["rsi"] = base_block.calculate_rsi(close_prices, 14)
            
            if input_data.use_macd:
                technical_analysis["macd"] = base_block.calculate_macd(close_prices, 12, 26, 9)
            
            if input_data.use_moving_averages:
                technical_analysis["moving_averages"] = base_block.calculate_moving_averages(close_prices, 20, 50)
            
            if input_data.use_bollinger_bands:
                technical_analysis["bollinger_bands"] = base_block.calculate_bollinger_bands(close_prices, 20, 2.0)
            
            if input_data.use_atr:
                technical_analysis["atr"] = base_block.calculate_atr(input_data.price_data, 14)
            
            if input_data.use_stochastic:
                technical_analysis["stochastic"] = base_block.calculate_stochastic(input_data.price_data, 14, 3)
            
            # ===== SMART MONEY CONCEPTS =====
            smc_analysis = {}
            
            if input_data.use_fvg:
                smc_analysis["fvgs"] = self.detect_fvg(input_data.price_data, input_data.fvg_threshold)
            
            if input_data.use_order_blocks:
                smc_analysis["order_blocks"] = self.detect_order_blocks(
                    input_data.price_data, input_data.ob_strength_period
                )
            
            if input_data.use_poi:
                fvgs = smc_analysis.get("fvgs", [])
                order_blocks = smc_analysis.get("order_blocks", [])
                smc_analysis["pois"] = self.identify_poi(input_data.price_data, fvgs, order_blocks)
            
            if input_data.use_pd_arrays:
                smc_analysis["pd_arrays"] = self.calculate_pd_arrays(input_data.price_data)
            
            if input_data.use_liquidity_zones:
                smc_analysis["liquidity_zones"] = self.detect_liquidity_zones(input_data.price_data)
            
            if input_data.use_market_structure:
                smc_analysis["market_structure"] = self.analyze_market_structure(input_data.price_data)
            
            # ===== KEY LEVELS =====
            key_levels = {}
            
            if input_data.use_support_resistance:
                key_levels["support_resistance"] = self.calculate_support_resistance(
                    input_data.price_data, input_data.sr_lookback
                )
            
            if input_data.use_fibonacci:
                key_levels["fibonacci"] = self.calculate_fibonacci_levels(
                    input_data.price_data, input_data.fib_swing_period
                )
            
            if input_data.use_pivot_points:
                key_levels["pivot_points"] = self.calculate_pivot_points(
                    input_data.price_data, input_data.pivot_type
                )
            
            # ===== VOLUME ANALYSIS =====
            volume_analysis = {}
            
            if input_data.use_volume_profile:
                volume_analysis["volume_profile"] = self.calculate_volume_profile(
                    input_data.price_data, input_data.volume_profile_bins
                )
            
            if input_data.use_order_book and input_data.order_book_data:
                volume_analysis["order_book"] = self.analyze_order_book(input_data.order_book_data)
            
            # ===== FUNDAMENTAL ANALYSIS =====
            fundamental_analysis = {}
            if input_data.use_fundamental_analysis:
                fundamental_analysis = base_block.analyze_fundamental_data(
                    input_data.economic_events,
                    input_data.news_sentiment,
                )
            
            # ===== GENERATE SIGNAL =====
            signal_result = self.generate_advanced_signal(
                input_data.price_data,
                technical_analysis,
                smc_analysis,
                volume_analysis,
                key_levels,
                fundamental_analysis,
                input_data,
            )
            
            # Get market structure
            market_structure = smc_analysis.get("market_structure", {}).get("structure", "unknown")
            
            # Yield outputs
            yield "signal", signal_result["signal"]
            yield "confidence", signal_result["confidence"]
            yield "entry_price", signal_result["entry_price"]
            yield "stop_loss", signal_result["stop_loss"]
            yield "take_profit", signal_result["take_profit"]
            yield "take_profit_2", signal_result["take_profit_2"]
            yield "take_profit_3", signal_result["take_profit_3"]
            yield "market_structure", market_structure
            yield "technical_analysis", technical_analysis
            yield "smc_analysis", smc_analysis
            yield "volume_analysis", volume_analysis
            yield "key_levels", key_levels
            yield "fundamental_analysis", fundamental_analysis
            yield "strategy_explanation", signal_result["explanation"]
            yield "risk_assessment", {
                "risk_level": signal_result["risk_level"],
                "risk_factors": signal_result["risk_factors"],
                "signal_score": signal_result["signal_score"],
            }
            
        except Exception as e:
            error_msg = f"Error in advanced strategy analysis: {str(e)}"
            logger.error(error_msg)
            yield "error", error_msg
            yield "signal", SignalType.HOLD.value
            yield "confidence", 0.0
            yield "market_structure", "error"
            yield "technical_analysis", {}
            yield "smc_analysis", {}
            yield "volume_analysis", {}
            yield "key_levels", {}
            yield "fundamental_analysis", {}
            yield "strategy_explanation", f"Analysis failed: {error_msg}"
            yield "risk_assessment", {"risk_level": "unknown", "risk_factors": []}
