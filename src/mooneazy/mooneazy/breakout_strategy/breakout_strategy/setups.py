'''
Fetches candle stick data from candles api using parameters from the 
config file. Applys the signals algorithms and trade setup algoriths 
to the candles
'''
from ...candles_api.candles_api import api
from . import config
from . import signals


def get_candles(symbol, interval, limit):
    parameters = {
        'symbol': symbol, 
        'interval': interval, 
        'limit': limit
    }
    candles = api.get_candles(parameters=parameters)
    return candles


def get_signal(symbol):
    trading_tf_intervals = config.TRADING_TF_INTERVALS
    trading_tf_limit = config.TRADING_TF_LIMIT
    htf_limit = config.HTF_LIMIT
    htf_intervals = config.HTF_INTERVALS

    htf1_candles = get_candles(symbol, htf_intervals[0], htf_limit)
    htf2_candles = get_candles(symbol, htf_intervals[1], htf_limit)
    signal_kwargs = {
        'trading_tf_candles': None,
        'htf1_candles': htf1_candles,
        'htf2_candles': htf2_candles,
        'lookback_left': config.LOOKBACK_LEFT,
        'min_opposite_candles': config.MIN_OPPOSITE_CANDLES,
        'ema_cross_periods': config.EMA_CROSS_PERIODS,
        'hull_period': config.HULL_PERIOD,
        'interval': None,
        'tp_rrrs': config.TP_RRRS,
        'sl_padding': config.SL_PADDING
    }
    trade_signals = []
    for interval in trading_tf_intervals:
        candles = get_candles(
            symbol=symbol,
            interval=interval,
            limit=trading_tf_limit
        )
        signal_kwargs['trading_tf_candles'] = candles
        signal_kwargs['interval'] = interval
        signal = signals.get_breakout_trade_signal(**signal_kwargs)
        if signal:
            trade_signals.extend(signal)
    return trade_signals


def get_trade_signals(supported_symbols=config.SUPPORTED_SYMBOLS):
    signals = []
    for symbol in supported_symbols:
        if trade_signals:= get_signal(symbol):
            signals.extend(trade_signals)
    return signals if signals else None 
