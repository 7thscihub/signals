# engulfing breakout signal data
# score = 3 (1 for breakout candle breaks emas 8 and 20 and 2 the breakout candle is an ema cross candle 
# i.e. its the candle at the exact time the the ema 8 crosses below ema 20 to create a bearish cross)
# the breakout candle touches hull 55 but the the previous 5 candles do not touch the hull 55


score_3_data = {
    'breakout_candles': [
        {"open": 65700.00, "high": 65850.00, "low": 65676.00, "close": 65820.00},  # Establishes the Lowest Low
        {"open": 65900.00, "high": 65976.43, "low": 65750.00, "close": 65780.00},  # Establishes the Highest High
        {"open": 65780.00, "high": 65910.00, "low": 65720.00, "close": 65890.00},
        {"open": 65890.00, "high": 65920.00, "low": 65700.00, "close": 65740.00},
        {"open": 65740.00, "high": 65860.00, "low": 65690.00, "close": 65710.00},
        {"open": 65700.00, "high": 65720.00, "low": 65550.00, "close": 65580.00},
        
    ],
    'ema_8_values': [65810.00, 65805.00, 65825.00, 65800.00, 65770.00, 65690.00],
    'ema_20_values': [65750.00, 65760.00, 65775.00, 65780.00, 65765.00, 65710.00],
    'hull_55_values': [65650.00, 65660.00, 65655.00, 65640.00, 65665.00, 65600.00],
    'score': 3,
    'min_opposite_candles': 2
}


score_5_data = {
    'breakout_candles': [
        {"open": 65700.00, "high": 65850.00, "low": 65676.00, "close": 65820.00},
        {"open": 65900.00, "high": 65976.43, "low": 65750.00, "close": 65780.00},
        {"open": 65780.00, "high": 65910.00, "low": 65720.00, "close": 65890.00},
        {"open": 65890.00, "high": 65920.00, "low": 65700.00, "close": 65740.00},
        {"open": 65740.00, "high": 65860.00, "low": 65690.00, "close": 65710.00},
        {"open": 65700.00, "high": 65720.00, "low": 65550.00, "close": 65580.00}
    ],
    'ema_8_values': [65810.00, 65805.00, 65825.00, 65800.00, 65770.00, 65690.00],
    'ema_20_values': [65750.00, 65760.00, 65775.00, 65780.00, 65765.00, 65710.00],
    'hull_55_values': [65600.00, 65800.00, 65800.00, 65800.00, 65600.00, 65800.00],
    'score': 5,
    'min_opposite_candles': 2

}


