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
    
    min_retracement_price = pullback_pivot['value'] - (
        impulse * min_follow_up_retracement_fib
    )
    
    pullback_range = [c for c in candles if c['time'] > pullback_pivot['time']]
    if not pullback_range:
        return False

    if is_bullish_pullback:
        hh_ll_price = min(candle['low'] for candle in pullback_range)
        return hh_ll_price < min_retracement_price
    else:
        hh_ll_price = max(candle['high'] for candle in pullback_range)
        return hh_ll_price > min_retracement_price


def get_swings(pivots_list) -> dict:
    impulse_list = []
    for i, pivot in enumerate(pivots_list):
        impulse = 0.0
        if i != 0:
            impulse = get_impulse(pivot, pivots_list[i - 1])
        impulse_list.append({
            'impulse': impulse,
            'pivot': pivot
        })

    max_swing = max(impulse_list, key=lambda x: abs(x['impulse']))
    other_swings = [e for e in impulse_list if (
        e != max_swing and e['pivot']['time'] > max_swing['pivot']['time']
    )]
    return { 'max_swing': max_swing, 'other_swings': other_swings }


def get_max_pullback(other_swings, direction):
    if direction == 'buy':
        return min(other_swings, key=lambda x: x['pivot']['value'], default={})
    if direction == 'sell':
        return max(other_swings, key=lambda x: x['pivot']['value'], default={})


def get_pullback_details(pivots_list, min_fib=0.382, max_fib=0.7):
    swings = get_swings(pivots_list)
    if not swings:
        return None
 
    max_swing = swings['max_swing']
    other_swings = swings['other_swings']
    max_impulse = max_swing['impulse']
    direction = 'buy' if max_impulse > 0 else 'sell'
    max_pullback = get_max_pullback(other_swings, direction)

    if not max_pullback:
        return None 
    if not util.is_significant_pullback(
        impulse=max_impulse,
        pullback=max_pullback['pivot']['value'],
        min_fib_retracement=min_fib,
        max_fib_retracement=max_fib
    ):
        return None

    pullback_details =  {
        'impulse_pivot': max_swing['pivot'],
        'pullback_pivot': max_pullback['pivot'],
        'direction': direction
    }
    return pullback_details


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
 
    if pullback and pullback['direction'] == trend and is_valid_pullback_level(
        candles, pullback, min_follow_up_retracement_fib=min_follow_up_retracement_fib
    ):
        return pullback
 
    return None





