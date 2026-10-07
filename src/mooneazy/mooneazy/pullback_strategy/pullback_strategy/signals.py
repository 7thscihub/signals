from typing import Literal
from pydantic import BaseModel 
from .pullback import get_valid_pullback_level
from .fakeouts import get_active_signals
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
        candles, 
        interval: str = '15min',  
        configs = Configs(),
        trend: Literal['buy', 'sell', ''] = ''
    ) -> dict[str, any] | None:

    lookback_left, lookback_right = configs.pullback_lookback_values 
    pullback_level = get_valid_pullback_level(
        candles=candles, 
        lookback_left=lookback_left, 
        lookback_right=lookback_right,
        trend=trend
    )

    if not pullback_level:
        return None

    kwargs = {
        'candles': candles, 
        'interval': interval,
        'buy_levels': [],
        'sell_levels': [],
        'fo_lookback': configs.fo_lookback,
    }
    
    if pullback_level['direction'] == 'buy':
        kwargs['buy_levels'].append(pullback_level['pullback_pivot'])
    elif pullback_level['direction'] == 'sell':
        kwargs['sell_levels'].append(pullback_level['pullback_pivot'])

    active_signals = get_active_signals(**kwargs)
    if not active_signals:
        return None

    sorted_signals = sorted(active_signals, key=lambda k: k['time'], reverse=True)
    active_signal = sorted_signals[0] | {'tp_rrrs': configs.tp_rrrs}
    trade_signal = make_trade_signal(
        signal=active_signal,
        tp_rrrs=configs.tp_rrrs,
        sl_padding=configs.sl_padding
    )

    return trade_signal or None

