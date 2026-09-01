
from mooneazy.breakout_strategy.breakout_strategy.emas import EmaCross
from mooneazy.breakout_strategy.breakout_strategy import errors
from mooneazy.candles_api.candles_api import api

def is_bullish_cross(htf_candles, slow_ema_period, fast_ema_period):
    cross = EmaCross(
        candles=htf_candles, 
        slow_ema_period=slow_ema_period, 
        fast_ema_period=fast_ema_period
    )
    if cross.is_bearish():
        return False
    return True

def get_htf_trends(
        htf1_candles:list[dict] | None = None, 
        htf2_candles:list[dict] | None = None, 
        slow_ema_period:int=20, 
        fast_ema_period:int=8
    )-> tuple[str, str]:

    htf1_trend = 'sell'
    htf2_trend = 'sell'
    if is_bullish_cross(htf1_candles, slow_ema_period, fast_ema_period):
        htf1_trend = 'buy'
    if is_bullish_cross(htf2_candles, slow_ema_period, fast_ema_period):
        htf2_trend = 'buy'  
    return htf1_trend, htf2_trend


def in_trend(
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
    if is_bullish_pullback == is_bullish_cross(
        htf_candles=higher_htf_candles,
        fast_ema_period=fast_ema,  
        slow_ema_period=slow_ema
        ):
        return True
    return False 


if __name__ == "__main__":
    htf1_candles = api.get_candles({'symbol': 'BTCUSDT', 'interval': '4h', 'limit': 200})
    htf2_candles = api.get_candles({'symbol': 'BTCUSDT', 'interval': '1d', 'limit': 200})
    htf_trends = get_htf_trends(htf1_candles=htf1_candles, htf2_candles=htf2_candles)
    
    print(f"HTF Trends: {htf_trends}")


