
from .emas import EmaCross
from . import errors

def is_bullish_cross(htf_candles, slow_ema_period, fast_ema_period):
    cross = EmaCross(
        candles=htf_candles, 
        slow_ema_period=slow_ema_period, 
        fast_ema_period=fast_ema_period
    )
    if cross.is_bearish():
        return False
    return True


def is_valid_pullback(
        htf_candles=None, 
        higher_htf_candles=None, 
        is_bullish_pullback=None,
        fast_ema: int = None,
        slow_ema: int = None
    ):
    if not slow_ema or not fast_ema:
        raise errors.ProvideFastAndSlowEmaValues
    if not htf_candles:
        raise errors.ProvideHTFCandles
    if is_bullish_pullback == is_bullish_cross(
        htf_candles=htf_candles, 
        fast_ema_period=fast_ema,  
        slow_ema_period=slow_ema
        ):
        return True
    if not higher_htf_candles:
        return False
    if is_bullish_pullback == is_bullish_cross(htf_candles=higher_htf_candles):
        return True
    return False 







