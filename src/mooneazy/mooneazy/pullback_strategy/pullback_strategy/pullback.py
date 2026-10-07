from collections import OrderedDict
from typing import Literal
from . import util
from . import config
from . import pivots
from . import errors


def get_pivots(trade_candles, lookback_left=config.LOOKBACK_LEFT, lookback_right=config.LOOKBACK_RIGHT):
    highs = pivots.get_highs(trade_candles, lookback_left, lookback_right)
    lows = pivots.get_lows(trade_candles, lookback_left, lookback_right)
    return util.combine_pivots(resistance_pivots=highs, support_pivots=lows)


def get_impulse(pivot, prev_pivot):
    return pivot['value'] - prev_pivot['value']


def get_impulse_list(pivots) -> list[dict]:
    impulse_list = []
    for i, pivot in enumerate(pivots):
        impulse = 0.0
        if i != 0:
            impulse = get_impulse(pivot, pivots[i - 1])
        impulse_list.append({
            'impulse': impulse,
            'pivot': pivot
        })
    return impulse_list 


def get_pullback_details(pivots, min_fib=0.382, max_fib=0.7):
    impulse_elements = get_impulse_list(pivots)

    if not impulse_elements:
        return None

    max_element = max(impulse_elements, key=lambda x: abs(x['impulse']))
    max_impulse = max_element['impulse']
    pullback_pivot = None
    direction = 'buy' if max_impulse > 0 else 'sell'

    prev_element = None
    for current_element in impulse_elements:
        if prev_element == max_element and util.is_significant_pullback(
                impulse=max_impulse,
                pullback=current_element['impulse'],
                min_fib_retracement=min_fib,
                max_fib_retracement=max_fib
            ):
            pullback_pivot = current_element['pivot']
            break
        prev_element = current_element

    if not pullback_pivot:
        return None

    return {
        'impulse_pivot': max_element['pivot'],
        'pullback_pivot': pullback_pivot,
        'direction': direction
    }


def get_valid_pullback_level(
        candles: list[dict] = None,
        lookback_left: int = 5,
        lookback_right: int = 10,
        trend: Literal['buy', 'sell'] = 'buy',
        min_fib: float = 0.382,
        max_fib: float = 0.7
    ):
    pivots = get_pivots(candles, lookback_left, lookback_right)
    pullback = get_pullback_details(pivots, min_fib=min_fib, max_fib=max_fib)
 
    if pullback and pullback['direction'] == trend:
        return pullback 

    return None




