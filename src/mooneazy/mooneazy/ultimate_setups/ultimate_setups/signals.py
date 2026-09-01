from .mooneazy.ultimate_setups.ultimate_setups.strategies.ultimate_setups import UltimateSetups
from .mooneazy.ultimate_setups.ultimate_setups.core.indicators import EmaCross
from .mooneazy.ultimate_setups.ultimate_setups.core.trading import get_trade


def get_ult_signal(
        htf1_candles, 
        htf2_candles, 
        trading_tf_candles,
        pivot_lookback, 
        fo_lookback, 
        ema_cross_periods, 
        interval, 
        sl_padding,
        tp_rrrs
    ):
    fast_ema_period, slow_ema_period = ema_cross_periods
    htf1_trend = 'buy' if EmaCross(
        candles=htf1_candles, 
        fast_ema_period=fast_ema_period,
        slow_ema_period=slow_ema_period
    ).is_bullish() else 'sell'
    htf2_trend = 'buy' if  EmaCross(
        candles=htf2_candles, 
        fast_ema_period=fast_ema_period,
        slow_ema_period=slow_ema_period
    ).is_bullish() else 'sell'
    ult_setups = UltimateSetups(
        candles=trading_tf_candles,
        fo_lookback=fo_lookback,
        pivot_lookback=pivot_lookback
    )
    signal = ult_setups.get_in_trend_signal(htf1_trend, htf2_trend)
    if not signal:
        return None
    signal['interval'] = interval
    tp1_rrr, tp2_rrr = tp_rrrs
    trade_signal = get_trade(
        signal=signal, tp1_rrr=tp1_rrr, tp2_rrr=tp2_rrr, sl_padding=sl_padding
    )
    return trade_signal or None
    

