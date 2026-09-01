PINBAR_FIB = 0.236

SIGNAL_UPTIME = {
    'dca': 1440, 
    'scalp': 60,
    'swing': 240,
}

ULTIMATE_SCALPING_SETTINGS = {
    "breakout_lookback": 5,
    "fo_lookback": 5,
    "pivot_lookback": 30,
    "default_symbol": "BTCUSDT",
    "default_quantity": 500,
    "stop_lose_padding": 0.0011,
    "tp2_rrr": 3,
    "tp1_rrr": 1.5,
    "min_opposite": 2,
    "trade_periods": {"30m": ["30m"], "4h": ["4h"], "1d": ["1d"]},
    "symbols": ["BTCUSDT", "ETHUSDT"],
    "default_period": "30m",
    "signal_uptime": 60,
    "max_breach": 4,
    "signal_quantity": {"5m": 180, "15m": 60, "30m": 500, "4h": 500},
    "trend": {'period': '1d', 'fast_ema': 8, 'slow_ema': 20},

}

ULTIMATE_SWING_SETTINGS = {
    "period": "4h",
    "setup_period": "4h",
    "trade_period": "4h",
    "pivot_lookback": 30,
    "fo_lookback": 5,
    "4h": {"setup_period": "4h", "trade_period": "4h"},
    "tp1_rrr": 3,
    "tp2_rrr": 10,

}

ULTIMATE_DCA_SETTINGS = {
    "setup_period": "1d",
    "pivot_lookback": 90,
    "tp1_rrr": 20,
    "tp2_rrr": 30,
    "trade_period": "5m",
}


TREND_SETTINGS = {
    "period": "1d",
    "fast_ema": 8,
    "slow_ema": 20,
}


MARKERS = {
    "buy_marker": {
        "position": 'belowBar',
        "color": '#05dff7',
        "shape": 'circle',
        "text": 'Buy',
    },
    "sell_marker": {
        "position": 'aboveBar',
        "color": '#f74e05',
        "shape": 'circle',
        "text": 'Sell',
    }
}


CHART_SETTINGS = {
    "pivot_types": ["high", "low"],
    "fib_levels": [0.8, 0.67, 0.618, 0.35],
    "pivots_gap": 20,
    "lookback": 5,
    "trendline_fibs": [0.45, 0.75],
    "range_quantity": 210

}

TRIGGER_CROSS = {
    "fast_ema": 8,
    "slow_ema": 20
}

REACTION_RANGE = {
    "lookback": CHART_SETTINGS["lookback"] * 2
}

TRENDLINE_SETTING = {
    "trendline_fibs": [0.75, 0.45],
    "trendline_pivot_spacings": 15,

}

RSI_SETTINGS = {
    "upper_band": 80,
    "lower_band": 20,
    "mid_band": 40,

}

RSI_REVERSAL_LEVELS = {
    "30m": 15,
    "4h": 15,
    "12h": 20,
    "1D": 25,
}

STOCHASTIC_RSI_SETTINGS = {
    "upper_band": 100,
    "lower_band": 0,
    "mid_band": 50,
    "k": 3,
    "d": 3,
    "min_lookback_range": CHART_SETTINGS["lookback"],
    "period": 14,
}

HULL_SUIT_SETTINGS = {
    "period": 55,
    "lookback": CHART_SETTINGS["lookback"]
}

TIMEFRAMES = {
    "default": "4h",
    "common_timeframe": ["5m", "15m", "30m", "1h", "2h", "4h", "8h", "12", "1D", "3D", "1W", "1M", ],
}

INTERVALS = {
    "default": "4h",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "8h": "8h",
    "12h": "12h",
    "1D": "1D",
    "3D": "3D",
    "1W": "1W",
    "1M": "1M",

}

LFT = INTERVALS["30m"]
MTF = INTERVALS["4h"]
HTF = INTERVALS["3D"]

SYMBOLS = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",

}

CVD_SETTINGS = {
    "intra_intervals": {
        "5m": "30s",
        "30m": "1m",
        "1h": "1m",
        "2h": "2m",
        "4h": "3m",
        "8h": "5m",
        "12h": "10m",
        "1D": "15m",
    },

    "quantity": 500,
    "pinbar_fib": 0.382
}

INDICATOR_QUANTITY = 500

TRIGGER_CROSS_SETTINGS = {
    "fast_ema": 8,
    "slow_ema": 20,
    "lookback": 5,
    "minimum_opposite_candles": 2,
    "sma_period": 14,

}

TRIGGER_BREAKOUT_SETTINGS = {
    "minimum_opposit_candles": (TRIGGER_CROSS_SETTINGS["lookback"] + 1) / 3,

}
