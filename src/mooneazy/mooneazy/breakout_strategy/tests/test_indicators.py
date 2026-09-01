import pytest
from mooneazy.breakout_strategy.breakout_strategy import emas, hma
import json
from mooneazy.candles_api.candles_api import api

CANDLES_FILE_PATH = 'tests/test_data/candles.json'
CANDLES = api.get_candles_from_json(CANDLES_FILE_PATH)

def test_ema_cross():
    cross = emas.EmaCross(
        candles=CANDLES,
        fast_ema_period=8,
        slow_ema_period=20
    )
    assert cross.is_bullish() == False
    assert cross.is_bearish() == True

def test_hma():
    breakout_hma = hma.BreakoutHMA(
        indicator_candles=CANDLES,
        period=55,
        lookback_left=5
    ).values()

    assert len(breakout_hma) == 6
    assert breakout_hma[-1] == 76245.06469173022

