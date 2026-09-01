
def define_range(candles, lookback=5):
    range_high = get_range_high(candles, lookback)
    range_low = get_range_low(candles, lookback)
    return [range_high, range_low]


def get_range_high(candles, lookback):
    sorted_by_highs = sorted(candles[:(len(candles) - lookback)], key=lambda k: k["high"], reverse=True)
    for candle in sorted_by_highs:
        if is_resistance_pivot(candles, candle, lookback):
            return candle


def get_range_low(candles, lookback):
    sorted_by_lows = sorted(candles[:(len(candles) - lookback)], key=lambda k: k["low"])
    for i in sorted_by_lows:
        for candle in candles:
            if i["time"] == candle["time"] and is_support_pivot(candles, candle, lookback):
                return candle


def is_support_pivot(candles, candle, lookback):
    candle_index = candles.index(candle)
    start_index = candle_index - lookback
    end_index = candle_index + lookback + 1

    if start_index < 0 or end_index > len(candles) - 1:
        return False

    candle_range = candles[start_index:end_index]

    return candle["low"] == min(candle["low"] for candle in candle_range)


def is_resistance_pivot(candles, candle, lookback):
    candle_index = candles.index(candle)
    start_index = candle_index - lookback
    end_index = candle_index + lookback + 1

    # check if there are enough candles, lookback padding left and right to be a pivot
    if start_index < 0 or end_index > len(candles) - 1:
        return False

    candle_range = candles[start_index:end_index]
    return candle["high"] == max(candle["high"] for candle in candle_range)


def is_same_candle(candle1, candle2):
    try:
        return candle1["time"] == candle2["time"]
    except TypeError:
        return False


def get_lower_lows(candles, lookback):
    """
    to get lower lows the slice of candles should start from range high to current candle
    """

    range_high = get_range_high(candles, lookback)
    last_range = candles[candles.index(range_high):]
    range_low = get_range_low(last_range, lookback)

    ll_range = last_range[:last_range.index(range_low) + lookback + 1]

    if range_low is None:
        return None

    sorted_by_lows = sorted(ll_range, key=lambda k: k["low"])

    pivots = [c for c in sorted_by_lows if is_support_pivot(ll_range, c, lookback)]

    for pivot in pivots:
        if next_pivot := get_next(pivots, pivot):
            if next_pivot["time"] > pivot["time"]:
                pivots = [pivot for pivot in pivots if pivot != next_pivot]
    pivots.append(range_low)
    return pivots


def get_higher_highs(candles, lookback):
    range_low = get_range_low(candles, lookback)
    last_range = candles[candles.index(range_low):]
    range_high = get_range_high(last_range, lookback)

    hh_range = last_range[:last_range.index(range_high) + lookback + 1]

    if range_high is None:
        return None

    sorted_by_highs = sorted(hh_range, key=lambda k: k["high"], reverse=True)

    pivots = [c for c in sorted_by_highs if is_resistance_pivot(hh_range, c, lookback)]

    for pivot in pivots:
        if next_pivot := get_next(pivots, pivot):
            if next_pivot["time"] > pivot["time"]:
                pivots = [pivot for pivot in pivots if pivot != next_pivot]
    pivots.append(range_high)
    return pivots


def get_next(elements: list, element):
    try:
        element_index = elements.index(element)
        return elements[element_index + 1]
    except (ValueError, IndexError):
        # element not in list of elements or element is last
        return None


def get_support_pivots(candles: list, lookback: int):
    support_pivots = []
    for i, candle in enumerate(candles):
        candle_index = i
        start_index = candle_index - lookback
        end_index = candle_index + lookback + 1

        if start_index < 0 or end_index > len(candles) - 1:
            continue

        lookback_candles = candles[start_index:end_index]
        if candle["low"] == min(c["low"] for c in lookback_candles):
            support_pivots.append(candle)

    return support_pivots


def get_lows(candles, lookback):
    lows = get_support_pivots(candles, lookback)
    for pivot in lows:
        for i in lows:
            if i["time"] > pivot["time"] and i["low"] < pivot["low"]:
                lows = [p for p in lows if p != pivot]

    for pivot in lows:
        if is_breached_support(candles, pivot):
            lows = [p for p in lows if p != pivot]
    return lows


def get_resistance_pivots(candles: list, lookback: int):
    resistance_pivots = []
    for i, candle in enumerate(candles):
        candle_index = i
        start_index = candle_index - lookback
        end_index = candle_index + lookback + 1

        if start_index < 0 or end_index > len(candles) - 1:
            continue

        lookback_candles = candles[start_index:end_index]
        if candle["high"] == max(c["high"] for c in lookback_candles):
            candle["breach_time"] = is_breached_resistance(candles, candle)
            resistance_pivots.append(candle)
    return resistance_pivots


def get_highs(candles, lookback):
    highs = get_resistance_pivots(candles, lookback)
    for pivot in highs:
        for i in highs:
            if i["time"] > pivot["time"] and i["high"] > pivot["high"]:
                highs = [p for p in highs if p != pivot]
    for pivot in highs:
        if is_breached_resistance(candles, pivot):
            highs = [p for p in highs if p != pivot]
    return highs


def is_breached_support(candles, pivot):
    count_breach = 0
    for candle in candles:
        if candle["time"] > pivot["time"] and candle["close"] < pivot["low"]:
            count_breach += 1
        if count_breach >= 4:
            return candle["time"]
    return None


def is_breached_resistance(candles, pivot):
    count_breach = 0
    for candle in candles:
        if candle["time"] > pivot["time"] and candle["close"] > pivot["high"]:
            count_breach += 1
        if count_breach >= 4:
            return candle["time"]
    return None

