from candles_api import api
from range_strategy import signals
from range_strategy import config


def get_candles(symbol, interval, limit):
    parameters = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    candles = api.get_candles(parameters=parameters)
    return candles


def get_trade_signal(symbol):
    HTF1_PARAMETERS = config.HTF1_PARAMETERS
    HTF2_PARAMETERS = config.HTF2_PARAMETERS
    TRADING_TF_PARAMETERS = config.SCALPING_CANDLES_PARAMETERS 

    htf1_candles = get_candles(symbol, HTF1_PARAMETERS[0], HTF1_PARAMETERS[1])
    htf2_candles = get_candles(symbol, HTF2_PARAMETERS[0], HTF2_PARAMETERS[1])
    trading_tf_candles = get_candles(
        symbol, TRADING_TF_PARAMETERS[0], TRADING_TF_PARAMETERS[1]
    )
    
    trade_signal = signals.get_trade_signals(
        trading_tf_candles=trading_tf_candles,
        htf1_candles=htf1_candles,
        htf2_candles=htf2_candles,
        pivot_lookback=config.PIVOT_LOOKBACK,
        fo_lookback=config.FO_LOOKBACK,
        ema_cross_periods=config.EMA_CROSS_PERIODS,
        tp_rrrs=config.TP_RRRS
    )
    return trade_signal


def get_trade_signals(supported_symbols):
    trade_signals = []
    for symbol in supported_symbols:
        signal = get_trade_signal(symbol)
        if signal:
            trade_signals.extend(signal)
    return trade_signals



