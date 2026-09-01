from mooneazy.pullback_strategy.pullback_strategy.pullback import get_valid_pullback_level
from mooneazy.pullback_strategy.pullback_strategy.fakeouts import get_active_signals
from mooneazy.pullback_strategy.pullback_strategy.trading import get_trade


def make_trade_signal(signal, tp_rrrs, sl_padding) -> dict:
    signal_type = (
        'impulse_pullback_' + signal['signal_type']
    )
    signal['signal_type'] = signal_type
    trade_signal = get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal


def get_trade_signal(
        htf_candles, 
        trading_tf_candles, 
        trading_interval: str = '15min', 
        ema_periods: tuple = (8, 20), 
        lookback_values: tuple = (5, 5), 
        fo_lookback: int = 5,
        tp_rrrs: tuple = (2, 5),
        sl_padding: int = 0.001,
    )->dict[str, any] | None:
    
    slow_ema, fast_ema = ema_periods
    lookback_left, lookback_right = lookback_values

    pullback_level = get_valid_pullback_level(
        htf_candles, trading_tf_candles, slow_ema, fast_ema, 
        lookback_left, lookback_right
    )
    # print(f'pullback_level: {pullback_level}')
    if not pullback_level:
        return None
    kwargs = {
        'candles': trading_tf_candles, 
        'interval': trading_interval,
        'buy_levels': [],
        'sell_levels': [],
        'fo_lookback': fo_lookback,
    }
    
    if pullback_level['is_bullish'] == True:
        kwargs['buy_levels'].append(pullback_level['pullback_pivot'])
    if pullback_level['is_bullish'] == False:
        kwargs['sell_levels'].append(pullback_level['pullback_pivot'])

    active_signals = get_active_signals(**kwargs)
    if not active_signals:
        return None
    sorted_signals = sorted(active_signals, key=lambda k :k['time'], reverse=True)
    active_signal = sorted_signals[0] | {'tp_rrrs': tp_rrrs}
    trade_signal = make_trade_signal(
        signal=active_signal,
        interval=trading_interval,
        sl_padding=sl_padding,
        tp_rrrs=tp_rrrs
    )

    return trade_signal or None


