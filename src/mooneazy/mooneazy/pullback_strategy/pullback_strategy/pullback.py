from collections import OrderedDict
from . import util
from . import htf_trend
from . import config
from . import pivots
from . import errors


def get_pivots(trade_candles, lookback_left=None, lookback_right=None):
    lookback_left = lookback_left or config.LOOKBACK_LEFT
    lookback_right = lookback_right or config.LOOKBACK_RIGHT

    highs = pivots.get_highs(trade_candles, lookback_left, lookback_right)
    lows = pivots.get_lows(trade_candles, lookback_left, lookback_right)
    return util.combine_pivots(resistance_pivots=highs, support_pivots=lows)


def get_impulse(pivot, prev_pivot):
    return pivot['value'] - prev_pivot['value']


def get_impulse_dict(pivots):

    impulse_dict = OrderedDict()
    for i, pivot in enumerate(pivots):
        impulse = 0
        if i != 0:
            impulse = get_impulse(pivot, pivots[i - 1])
        # print(f'{i}, {impulse}')
        impulse_dict[impulse] = pivot
        impulse_dict.move_to_end(impulse)
    return impulse_dict


def get_pullback_details(pivots, min_fib=0.382, max_fib=0.7):
    # print(f'from pullback: pivots: {pivots}')
    impulse_dict = get_impulse_dict(pivots)
    # print(f'from pullback: impulse_dict: {impulse_dict.keys()}')
    if not impulse_dict:
        return None
    max_impulse = max(impulse_dict.keys(), key=abs)
    pullback_pivot = None
    is_bullish = True if max_impulse > 0 else False
    # print(f'from pullback: impulse_dict: {impulse_dict}')
    prev_impulse: float = None
    for impulse in impulse_dict:
        if prev_impulse == max_impulse and util.is_significant_pullback(
                impulse=max_impulse,
                pullback=impulse,
                min_fib_retracement=min_fib,
                max_fib_retracement=max_fib
            ):
            pullback_pivot = impulse_dict[impulse]
        prev_impulse = impulse
        # print(f'from pullback details: {current_key}')
    if not pullback_pivot:
        return None
    return {
        'impulse_pivot': impulse_dict[max_impulse],
        'pullback_pivot': pullback_pivot,
        'is_bullish': is_bullish
    }
        

def get_valid_pullback_level(
        htf_candles: list[dict] = None, 
        trade_candles: list[dict] = None,
        slow_ema: int = 20,
        fast_ema: int =8,
        lookback_left: int = 10,
        lookback_right: int = 30
    ): 
    if not htf_candles or not trade_candles:
        raise errors.ProvideSetupCandles
    pivots = get_pivots(trade_candles, lookback_left, lookback_right)
    pullback_details = get_pullback_details(pivots)

    if not pullback_details:
        return None
    is_bullish_pullback = pullback_details['is_bullish']

    if htf_trend.is_valid_pullback(
        htf_candles=htf_candles, 
        is_bullish_pullback=is_bullish_pullback,
        fast_ema=fast_ema,
        slow_ema=slow_ema
        ):
        return pullback_details
    return None
