from mooneazy.breakout_strategy.breakout_strategy.breakout import BreakOut, is_engulfing_breakout, breaks_emas, is_cross
from mooneazy.breakout_strategy.tests.test_data import breakout_data

def test_is_engulfing_breakout():
    breakout_candles = breakout_data.score_5_data['breakout_candles']
    min_opposite_candles = 2

    assert is_engulfing_breakout(
        lookback_candles=breakout_candles[:-1], 
        breakout_candle=breakout_candles[-1], 
        min_opposit=min_opposite_candles
    ) == False


def test_breaks_emas():
    breakout_candles = breakout_data.score_3_data['breakout_candles']
    fast_ema_values = breakout_data.score_3_data['ema_8_values']
    slow_ema_values = breakout_data.score_3_data['ema_20_values']

    assert breaks_emas(
        breakout_candle=breakout_candles[-1], 
        fast_ema_value=fast_ema_values[-1], 
        slow_ema_value=slow_ema_values[-1]
    ) == True


def test_is_cross():
    breakout_candles = breakout_data.score_3_data['breakout_candles']
    fast_ema_values = breakout_data.score_3_data['ema_8_values']
    slow_ema_values = breakout_data.score_3_data['ema_20_values']

    assert is_cross(
        candle=breakout_candles[-1], 
        fast_ema_values=fast_ema_values, 
        slow_ema_values=slow_ema_values
    ) == True


def test_breakout_score_3():
    data = breakout_data.score_3_data
    breakout_candles = data['breakout_candles']
    fast_ema_values = data['ema_8_values']
    slow_ema_values = data['ema_20_values']
    hull_values = data['hull_55_values']
    min_opposite_candles = data['min_opposite_candles']

    breakout = BreakOut(
        breakout_candles=breakout_candles,
        fast_ema_values=fast_ema_values,
        slow_ema_values=slow_ema_values,
        hull_values=hull_values,
        min_opposite_candles=min_opposite_candles
    )
    assert breakout.is_engulfing() == False
    assert breakout.is_valid() == False
    assert breakout.get_score() == data['score']
    assert breakout.is_cross() == True
    assert breakout.is_tight_hull() == False
    assert breakout.breaks_emas() == True


def test_breakout_score_5():
    breakout_candles = breakout_data.score_5_data['breakout_candles']
    fast_ema_values = breakout_data.score_5_data['ema_8_values']
    slow_ema_values = breakout_data.score_5_data['ema_20_values']
    hull_values = breakout_data.score_5_data['hull_55_values']
    min_opposite_candles = 2
    
    breakout = BreakOut(
        breakout_candles=breakout_candles,
        fast_ema_values=fast_ema_values,
        slow_ema_values=slow_ema_values,
        hull_values=hull_values,
        min_opposite_candles=min_opposite_candles
    )
    
    assert breakout.is_engulfing() == False
    assert breakout.breaks_emas() == True
    assert breakout.is_cross() == True
    assert breakout.is_tight_hull() == True
    assert breakout.get_score() == breakout_data.score_5_data['score']
    assert breakout.is_valid() == False
    
