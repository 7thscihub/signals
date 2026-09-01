from mooneazy.breakout_strategy.breakout_strategy.htf_trend import in_trend
from mooneazy.candles_api.candles_api.api import get_candles_from_json

CANDLES = get_candles_from_json('tests/test_data/candles.json')


def test_bullish_pullback():
    htf_in_trend = in_trend(
        htf_candles=CANDLES,
        is_bullish_pullback=True,
        fast_ema=8,
        slow_ema=20
    )
    assert htf_in_trend == False
    

def test_bearish_pullback():
    htf_in_trend = in_trend(
        htf_candles=CANDLES,
        is_bullish_pullback=False,
        fast_ema=8,
        slow_ema=20
    )
    assert htf_in_trend == True

