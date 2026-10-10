from typing import Literal
from pydantic import BaseModel 
from .pullback import get_valid_pullback_level
from .fakeouts import get_all_signals
from .trading import get_trade


class Configs(BaseModel):
    pullback_lookback_values: tuple[int, int] = (5, 5)
    fo_lookback: int = 5
    tp_rrrs: tuple[float, float] = (2.0, 5.0)
    sl_padding: float = 0.001


def make_trade_signal(signal: dict, tp_rrrs: tuple, sl_padding: float) -> dict:
    signal_type = 'impulse_pullback_' + signal['signal_type']
    signal['signal_type'] = signal_type
    
    trade_signal = get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal


def get_trade_signal(
        candles,  interval: str, trend: str, configs = Configs()
    ) -> dict[str, any] | None:
    lookback_left, lookback_right = configs.pullback_lookback_values 
    pullback_level = get_valid_pullback_level(
        candles=candles, 
        lookback_left=lookback_left, 
        lookback_right=lookback_right,
        trend=trend
    )

    if not pullback_level:
        return []

    kwargs = {
        'candles': candles, 
        'buy_levels': [],
        'sell_levels': [],
        'fo_lookback': configs.fo_lookback,
    }
    
    if pullback_level['direction'] == 'buy':
        kwargs['buy_levels'].append(pullback_level['pullback_pivot'])
    elif pullback_level['direction'] == 'sell':
        kwargs['sell_levels'].append(pullback_level['pullback_pivot'])

    all_signals = get_all_signals(**kwargs)
    if not all_signals:
        return []

    sorted_signals = sorted(
        all_signals, key=lambda k: k['trigger_candle']['time'], reverse=True
    )
    latest_signal = sorted_signals[0] | {'tp_rrrs': configs.tp_rrrs}
    latest_signal['interval'] = interval
    trade_signal = make_trade_signal(
        signal=latest_signal,
        tp_rrrs=configs.tp_rrrs,
        sl_padding=configs.sl_padding
    )

    return trade_signal or []



class Pullback:
    def __init__(self, candles, interval: str, trend: str, configs = Configs()):
        self._candles = candles
        self._interval = interval
        self._trend = trend
        self._configs = configs
        self._range_lookback = self._configs.range_lookback
    
    def get_trade_signals(self):
        signals = []
        candles = self._candles
        len_candles = len(candles)
        if len_candles <= self._range_lookback:
            return signals
        for candle_index in range(self._range_lookback, len(candles)-1):
            candle_signal = get_trade_signal(
                candles=candles[:candle_index + 1],
                interval=self._interval,
                trend=self._trend,
                configs=self._configs
            )
            if candle_signal:
                signals.append(candle_signal)
        return signals 
  
    def get_latest_signals(self):
        signals = self.get_trade_signals()
        if signals:
            return [signals[-1]]
        return []







