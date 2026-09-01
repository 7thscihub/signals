from mooneazy.breakout_strategy.breakout_strategy.breakout import BreakOut, is_bullish
from mooneazy.breakout_strategy.breakout_strategy.emas import get_breakout_ema_values
from mooneazy.breakout_strategy.breakout_strategy.hma import BreakoutHMA
from mooneazy.breakout_strategy.breakout_strategy.trading import get_trade


def make_trade_signal(breakout_candle, interval, tp_rrrs, sl_padding, score):
    lookback_hl = breakout_candle['high']
    signal_type = 'engulfing_breakout_sell'
    if is_bullish(breakout_candle):
        lookback_hl = breakout_candle['low']
        signal_type = 'engulfing_breakout_buy'
    signal = {
        'trigger_candle': breakout_candle,
        'lookback_hl': lookback_hl,
        'signal_type': signal_type,
        'interval': interval,
        'score': score
    }
    trade_signal = get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal


def get_indicator_values(
        indicator_candles, 
        ema_cross_periods = (8, 20),
        hull_period = 55, 
        lookback_left = 6
    ):
    breakout_lookback = lookback_left
    fast_ema_period = min(ema_cross_periods)
    slow_ema_period = max(ema_cross_periods)
    fast_emas, slow_emas = get_breakout_ema_values(
        indicator_candles=indicator_candles,
        fast_ema=fast_ema_period,
        slow_ema=slow_ema_period,
        lookback=breakout_lookback
    )
    breakout_hull_values = BreakoutHMA(
        indicator_candles = indicator_candles,
        period = hull_period, 
        lookback_left = breakout_lookback
    ).values()

    return fast_emas, slow_emas, breakout_hull_values


def get_breakout_trade_signal(
        trading_tf_candles, 
        htf_trends,
        lookback_left,
        min_opposite_candles,
        ema_cross_periods,
        hull_period,
        interval,
        tp_rrrs,
        sl_padding,
        min_score = 6
    ):
    print(f"Checking lookback_left: {lookback_left}")
    breakout_candles = trading_tf_candles[-lookback_left:]
    fast_emas, slow_emas, hull_values = get_indicator_values(
        indicator_candles=trading_tf_candles, 
        ema_cross_periods=ema_cross_periods, 
        hull_period=hull_period, 
        lookback_left=lookback_left
    )
    htf1_trend, htf2_trend = htf_trends
    breakout = BreakOut(
        breakout_candles=breakout_candles,
        fast_ema_values=fast_emas,
        slow_ema_values=slow_emas,
        hull_values=hull_values,
        min_opposite_candles=min_opposite_candles
    )
    print(f"Checking Length Candles {len(breakout.breakout_candles)}")
    if breakout_signal := breakout.get_in_trend_breakout(
        min_score=min_score, htf1_trend=htf1_trend, htf2_trend=htf2_trend
        ):
        trade_signal = make_trade_signal(
            breakout_candle=breakout_signal['trigger_candle'], 
            interval=interval,
            tp_rrrs=tp_rrrs,
            sl_padding=sl_padding,
            score=breakout_signal['score']
        )
        return trade_signal
    return None
           
