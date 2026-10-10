def candle(data):
    open_, high, low, close = data
    return {
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
    }


def levels(values):
    return [{'value': value} for value in values]


CANDLE_BULLISH = candle((100, 110, 95, 108))

CANDLE_BEARISH = candle((108, 110, 95, 100))

CANDLE_DOJI = candle((100, 105, 95, 100))


LOOKBACK_BULLISH = [
    candle((100, 105, 98, 103)),
    candle((103, 106, 101, 105)),
    candle((105, 108, 103, 107)),
]


LOOKBACK_BEARISH = [
    candle((105, 107, 101, 102)),
    candle((102, 104, 98, 100)),
    candle((100, 102, 95, 97)),
]


LOOKBACK_MIXED = [
    candle((100, 105, 98, 103)),
    candle((103, 105, 98, 100)),
    candle((100, 104, 97, 102)),
    candle((102, 104, 96, 98)),
]


BULLISH_BREAKOUT = candle((99, 115, 99, 112))

BEARISH_BREAKOUT = candle((106, 106, 90, 93))


TOUCHING_CANDLE = candle((100, 110, 90, 105))

NOT_TOUCHING_CANDLE = candle((100, 105, 95, 102))


FAST_EMAS_BULLISH_CROSS = levels([100, 105])

SLOW_EMAS_BULLISH_CROSS = levels([105, 103])


FAST_EMAS_BEARISH_CROSS = levels([105, 100])

SLOW_EMAS_BEARISH_CROSS = levels([100, 103])


EMA_VALUES = levels([100, 101, 102, 103, 104])

HULL_VALUES = levels([100, 101, 102])


BREAKOUT_CANDLES = [
    candle((105, 110, 100, 102)),
    candle((102, 108, 98, 100)),
    candle((100, 106, 97, 104)),
    candle((104, 115, 99, 112)),
]
