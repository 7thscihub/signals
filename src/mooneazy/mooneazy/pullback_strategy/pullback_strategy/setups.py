from mooneazy.candles_api.candles_api import api
from mooneazy.pullback_strategy.pullback_strategy import signals
from mooneazy.pullback_strategy.pullback_strategy import config

def get_setup_signal(symbol):
    HTF_INTERVAL, HTF_LIMIT = config.HTF_ARGS
    TRADING_TF_INTERVAL, TRADING_TF_LIMIT = config.TRADE_TF_ARGS
    EMA_PERIODS = config.EMA_PERIODS
    LOOKBACK_VALUES = config.LOOKBACK_VALUES

    htf_params = {'symbol': symbol,'interval': HTF_INTERVAL, 'limit': HTF_LIMIT}
    trading_tf_parameters = {
        'symbol': symbol,'interval': TRADING_TF_INTERVAL, 'limit': TRADING_TF_LIMIT
    }
    htf_candles = api.get_candles(htf_params)
    trading_candles = api.get_candles(trading_tf_parameters)

    trade_signal = signals.get_trade_signal(
        htf_candles=htf_candles,
        trading_candles=trading_candles,
        trading_interval=TRADING_TF_INTERVAL,
        ema_periods=EMA_PERIODS,
        lookback_values=LOOKBACK_VALUES[:-1],
        fo_lookback=LOOKBACK_VALUES[-1]
    )
    return trade_signal


def get_setup_signals(symbols:list = []):
    if not symbols:
        symbols = config.SUPPORTED_SYMBOLS
    signals = []
    for symbol in symbols:
        symbol_signal = get_setup_signal(symbol)
        if symbol_signal:
            signals.append(symbol_signal)

    return signals or None

    





