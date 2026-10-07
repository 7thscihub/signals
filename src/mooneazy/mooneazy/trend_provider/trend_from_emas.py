from ..breakout_strategy.breakout_strategy.emas import EmaCross


def is_bullish_cross(htf_candles, slow_ema_period, fast_ema_period):
    cross = EmaCross(
        candles=htf_candles, 
        slow_ema_period=slow_ema_period, 
        fast_ema_period=fast_ema_period
    )
    if cross.is_bearish():
        return False
    return True


def get_trend_from_emas(htf_candles:list[dict], ema_periods=(8, 20))-> str:
    slow_ema_period = max(ema_periods)
    fast_ema_period = min(ema_periods)
    if is_bullish_cross(htf_candles, slow_ema_period, fast_ema_period):
        return 'buy'
    return 'sell'



