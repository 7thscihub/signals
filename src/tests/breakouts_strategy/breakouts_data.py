"""
Test data for Breakouts tests.
"""


def candle(time=1_000, open=100, high=110, low=90, close=105, volume=1000,):
    return {
        "time": time,
        "open": open,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


CANDLES = [
    candle(time=i)
    for i in range(150)
]


FAST_EMA_VALUES = [
    100 + i
    for i in range(150)
]

SLOW_EMA_VALUES = [
    99 + i
    for i in range(150)
]

HULL_VALUES = [
    101 + i
    for i in range(150)
]


EMA_CROSSES = [
    {
        "time": 100,
        "direction": "bullish",
    },
    {
        "time": 200,
        "direction": "bearish",
    },
]


BREAKOUT_SLICES = {
    "breakout_candles": CANDLES[-20:],
    "fast_ema_values": FAST_EMA_VALUES[-20:],
    "slow_ema_values": SLOW_EMA_VALUES[-20:],
    "hull_values": HULL_VALUES[-20:],
}


BREAKOUT_SIGNAL = {
    "trigger_candle": CANDLES[-1],
    "score": 8,
}


BREAKOUT_SIGNAL_2 = {
    "trigger_candle": CANDLES[-2],
    "score": 7,
}


TRADE_SIGNAL = {
    "symbol": "BTCUSDT",
    "direction": "BUY",
    "entry": 105,
    "sl": 100,
    "tp1": 110,
    "score": 8,
}


TRADE_SIGNAL_2 = {
    "symbol": "ETHUSDT",
    "direction": "BUY",
    "entry": 200,
    "sl": 195,
    "tp1": 210,
    "score": 7,
}

