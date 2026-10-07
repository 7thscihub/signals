from .strategies.ultimate_setups import UltimateSetups
from .core.indicators import EmaCross
from .core.trading import get_trade


def get_ult_signal(candles, configs, interval, trend:str = ''):
    ult_setups = UltimateSetups(
        candles=candles,
        fo_lookback=configs.fo_lookback,
        pivot_lookback=configs.pivot_lookback
    )
    if not trend:
        signal = ult_setups.get_signal()
    else:
        signal = ult_setups.get_in_trend_signal(trend=trend)
    if not signal:
        return None
    signal['interval'] = interval
    tp1_rrr, tp2_rrr = configs.tp_rrrs
    trade_signal = get_trade(
        signal=signal, tp1_rrr=tp1_rrr, tp2_rrr=tp2_rrr, sl_padding=configs.sl_padding
    )
    return trade_signal or None


def get_ult_signals(candles, configs, interval, trend:str = ''):
    ult_setups = UltimateSetups(
        candles=candles,
        fo_lookback=configs.fo_lookback,
        pivot_lookback=configs.pivot_lookback
    )
    if not trend:
        signals = ult_setups.get_signals()
    else:
        signals = ult_setups.get_in_trend_signals(trend=trend)
    if not signals:
        return []
    trade_signals = []
    for signal in signals:
        signal['interval'] = interval
        tp1_rrr, tp2_rrr = configs.tp_rrrs
        trade_signal = get_trade(
            signal=signal, tp1_rrr=tp1_rrr, tp2_rrr=tp2_rrr, sl_padding=configs.sl_padding
        )
        if trade_signal:
            trade_signals.append(trade_signal)
    return trade_signals



