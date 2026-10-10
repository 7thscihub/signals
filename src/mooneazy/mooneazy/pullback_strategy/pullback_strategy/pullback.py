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


def is_valid_pullback_level(
        candles: list[dict], 
        pullback_details: dict, 
        min_follow_up_retracement_fib: float = 0.7
    ) -> bool:
    """
    Checks whether the lowest candle low (bearish pullback) 
    or highest candle high (bullish pullback)
    breaks the minimum retracement size required to validate the pivot point.
    """
    pullback_pivot = pullback_details['pullback_pivot']
    impulse_pivot = pullback_details['impulse_pivot']
    impulse = pullback_pivot['value'] - impulse_pivot['value']
    is_bullish_pullback = pullback_details['direction'] == 'buy'
    
    min_retracement_price = pullback_pivot['value'] - (impulse * min_follow_up_retracement_fib)
    
    pullback_range = [c for c in candles if c['time'] > pullback_pivot['time']]
    if not pullback_range:
        return False

    if is_bullish_pullback:
        hh_ll_price = min(candle['low'] for candle in pullback_range)
        return hh_ll_price < min_retracement_price
    else:
        hh_ll_price = max(candle['high'] for candle in pullback_range)
        return hh_ll_price > min_retracement_price


def get_impulse_list(pivots_list) -> list[dict]:
    impulse_list = []
    for i, pivot in enumerate(pivots_list):
        impulse = 0.0
        if i != 0:
            impulse = get_impulse(pivot, pivots_list[i - 1])
        impulse_list.append({
            'impulse': impulse,
            'pivot': pivot
        })
    return impulse_list


def get_pullback_details(pivots_list, min_fib=0.382, max_fib=0.7):
    impulse_elements = get_impulse_list(pivots_list)
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
        trend: Literal['buy', 'sell', None] = None,
        min_fib: float = 0.3,
        max_fib: float = 0.5,
        min_follow_up_retracement_fib: float = 0.7
    ):
    if not candles:
        return None
 
    pivots_list = get_pivots(candles, lookback_left, lookback_right)
    pullback = get_pullback_details(pivots_list, min_fib=min_fib, max_fib=max_fib)
 
    if pullback and pullback['direction'] == trend:
        if is_valid_pullback_level(candles, pullback, min_follow_up_retracement_fib=min_follow_up_retracement_fib):
            return pullback
 
    return None





