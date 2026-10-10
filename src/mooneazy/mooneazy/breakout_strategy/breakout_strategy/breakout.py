
def resolve_level(level:dict | int | float)-> float:
    """
    extracts level values for levels passed as dicts
    and return a list of int
    """
    if isinstance(level, dict):
        level = level["value"]
    return level

def is_bullish(candle) -> bool:
    return candle['close'] > candle['open']


def is_valid_min_oposite(lookback_candles, breakout_candle, min_oposit=None):
    if not min_oposit:
        min_oposit = len(lookback_candles) / 3
    count_bearish = 0
    count_bullish = 0
    for candle in lookback_candles:
        if is_bullish(candle):
            count_bullish += 1
        if not is_bullish(candle):
            count_bearish += 1
    if is_bullish(breakout_candle) and count_bearish >= min_oposit:
        return True
    if not is_bullish(breakout_candle) and count_bullish >= min_oposit:
        return True
    return False

def is_bad_candle(candle, range_high, range_low, multiplier: float=(0.5, 1.0)):
    """
    a bad candle is either too big or stretches too far beyond 
    the range of the lookback candles.
    """
    range_size = range_high - range_low
    close_multiplier = max(multiplier)
    hl_multiplier = min(multiplier)
    close_safe_zone_size = range_size * close_multiplier
    hl_safe_zone_size = range_size * hl_multiplier
    if is_bullish(candle):
        safe_close = range_high + close_safe_zone_size
        safe_low = range_low - hl_safe_zone_size
        return candle['close'] > safe_close or candle['low'] < safe_low
    safe_close = range_low - close_safe_zone_size
    saffe_high = range_high + hl_safe_zone_size
    return candle['close'] < safe_close or candle['high'] > saffe_high


def is_engulfing_breakout(lookback_candles, breakout_candle, min_opposit):
    max_high = max(candle['high'] for candle in lookback_candles)
    min_low = min(candle['low'] for candle in lookback_candles)
    mid_range = (max_high - min_low) / 2 + min_low
    if is_bad_candle(breakout_candle, range_high=max_high, range_low=min_low):
        return False
    if not is_valid_min_oposite(lookback_candles, breakout_candle, min_opposit):
        return False
    if is_bullish(breakout_candle):
        return breakout_candle['low'] < mid_range and breakout_candle['close'] > max_high
    return breakout_candle['high'] > mid_range and breakout_candle['close'] < min_low

def breaks_level(candle, level):
    if not isinstance(level, (int, float)):
        level = level['value']
    if is_bullish(candle):
        return candle['close'] > level > candle['low']
    return candle['close'] < level < candle['high']
    

def breaks_emas(breakout_candle, fast_ema_value, slow_ema_value):
    return breaks_level(
        breakout_candle, fast_ema_value
    ) and breaks_level(breakout_candle, slow_ema_value)


def touches(candle, value):
    value = resolve_level(value)
    return candle['high'] > value > candle['low']


def count_indicator_touches(candles, indicator_values):
    correspnding_candles = candles[-len(indicator_values):]
    count_touches = 0
    for i, value in enumerate(indicator_values):
        candle = correspnding_candles[i]
        if touches(candle, value):
            count_touches += 1

    return count_touches
        

def is_tight_indicator(no_of_touches, min_touches):
    return no_of_touches >= min_touches


def is_cross(candle, fast_ema_values, slow_ema_values):
    fast_ema_value = resolve_level(fast_ema_values[-1])
    prev_fast_ema_value = resolve_level(fast_ema_values[-2])
    slow_ema_value = resolve_level(slow_ema_values[-1])
    prev_slow_ema_value = resolve_level(slow_ema_values[-2])

    if not breaks_emas(candle, fast_ema_value, slow_ema_value):
        return False
    if is_bullish(candle):
        if fast_ema_value > slow_ema_value and (
            prev_fast_ema_value <= prev_slow_ema_value
            ):
            return True

    return  fast_ema_value < slow_ema_value and (
        prev_fast_ema_value >= prev_slow_ema_value
    )  
    

class BreakOut:
    def __init__(
            self, breakout_candles, fast_ema_values, 
            slow_ema_values, hull_values, min_opposite_candles
        ):
        self.breakout_candles = breakout_candles
        self.lookback_candles = breakout_candles[: -1]
        self.breakout_candle = breakout_candles[-1]
        self.min_opposit = min_opposite_candles
        self.fast_ema_values = fast_ema_values
        self.slow_ema_values = slow_ema_values
        self.breakout_hull_values = hull_values[-len(self.breakout_candles):]

        self._hull_touches = self.get_hull_touches()
        self._score = self.calculate_score()
        

    def is_cross(self):
        return is_cross(
            self.breakout_candle, 
            self.fast_ema_values, 
            self.slow_ema_values
        )

    def get_hull_touches(self):
        return count_indicator_touches(
            candles=self.breakout_candles,
            indicator_values=self.breakout_hull_values 
        )
    
    def is_tight_hull(self, min_touches=3):
        hull_touches = self._hull_touches
        if not min_touches:
            min_touches = len(self.breakout_candles)/2
        return hull_touches >= min_touches
    
    def is_tight_fast_emas(self, min_touches=3):  
        touches = count_indicator_touches(
            candles=self.breakout_candles,
            indicator_values=self.fast_ema_values[-len(self.breakout_candles):]
        )
        return is_tight_indicator(touches, min_touches=min_touches)

    def is_tight_slow_emas(self, min_touches=3):
        touches = count_indicator_touches(
            candles=self.breakout_candles,
            indicator_values=self.slow_ema_values[-len(self.breakout_candles):]
        )
        return is_tight_indicator(touches, min_touches=min_touches)

    def breaks_emas(self):
        return breaks_emas(
            self.breakout_candle, 
            self.fast_ema_values[-1], 
            self.slow_ema_values[-1]
        )
    
    def is_engulfing(self):
        return is_engulfing_breakout(
            self.lookback_candles, 
            self.breakout_candle, 
            self.min_opposit
        )
    
    def calculate_score(self):
        score = 0
        if not self.is_cross() or not self.breaks_emas():
            return 0
        if self.is_engulfing():
            score += 5
        if self.is_cross:
            score += 2
        if self.is_tight_hull(): 
            score += 1
        if self.is_tight_fast_emas():
            score += 1
        if self.is_tight_slow_emas():
            score += 1
        return score

    def is_valid(self, min_score=8):
        return self._score >= min_score 

    def get_score(self):
        return self._score

    def get_in_trend_breakout(self, min_score:int=8, trend:str='')->dict[str:list]:
        if not self.is_valid(min_score=min_score):
            return None
        signal_trend = 'buy' if is_bullish(self.breakout_candle) else 'sell'
        if signal_trend == trend:
            return {'trigger_candle': self.breakout_candle, 'score': self._score}
        return None 


