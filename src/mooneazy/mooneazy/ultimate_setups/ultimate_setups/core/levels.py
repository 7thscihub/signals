from mooneazy.ultimate_setups.ultimate_setups.core import pivots


def resistance_fib_prices(range, fib_levels, lookback):
	range_high, range_low = pivots.define_range(range, lookback)
	print(range_low["low"])
	fib_prices = []
	for level in fib_levels:

		price = level * (range_high["high"] - range_low["low"]) + range_low["low"]
		fib_prices.append(price)

	return fib_prices


def support_fib_prices(range, fib_levels, lookback):
	"""
	finds and returns the corresponding asset prices for the fib levels within the range
	"""
	range_high, range_low = pivots.define_range(range, lookback)
	fib_prices = []
	for level in fib_levels:
		price = (1 - level) * (range_high["high"] - range_low["low"]) + range_low["low"]
		fib_prices.append(price)

	return fib_prices


def get_significant_lows(range, lookback, fib_levels, gap):
	"""
	finds the lows that are within the lowest and the highest fib levels
	returns:
	list[dict] of support pivot candles that are within significant fib levels
	"""
	range_high, range_low = pivots.define_range(range, lookback)
	lows = pivots.get_lows(range, lookback)
	fib_prices = support_fib_prices(range, fib_levels, lookback)
	print(fib_prices)
	significant_lows = []
	for low in lows:
		if low["low"] <= max(fib_prices) and low["low"] >= min(fib_prices):
			significant_lows.append(low)

	decongested_pivots = decongest_lows(range, gap, significant_lows)
	decongested_pivots.append(range_low)
	decongested_pivots = sorted(decongested_pivots, key=lambda k: k["low"])

	return decongested_pivots


def get_significant_highs(range, lookback, fib_levels, gap):
	"""
	finds the most significant highs that are within the lowest and the highest fib levels
	returns:
	list[dict] of support pivot candles that are within significant fib levels
	"""
	range_high, range_low = pivots.define_range(range, lookback)
	highs = pivots.get_highs(range, lookback)
	fib_prices = resistance_fib_prices(range, fib_levels, lookback)
	# print(f"fib prices: {fib_prices}")
	significant_highs = []
	for high in highs:
		if high["high"] <= max(fib_prices) and high["high"] >= min(fib_prices):
			significant_highs.append(high)
		# else:
			# print(f"high:{high['high']}, max fib{max(fib_prices)}")
	decongested_pivots = decongest_highs(range, gap, significant_highs)
	decongested_pivots.append(range_high)
	decongested_pivots = sorted(decongested_pivots, key=lambda k: k["high"], reverse=True)

	# return significant_highs
	return decongested_pivots


def decongest_lows(range, gap, congested_pivots):
	"""
	find and return the strongest pivot levels when pivots are closely positions to each other
	The strongest pivots with the highest previous swing highs
	"""
	range_high, range_low = pivots.define_range(range)
	range_height = range_high["high"] - range_low["low"]
	spacing = range_height * gap / 100
	print(f"spacing: {spacing}, range_height{range_height}")
	decongested_pivots = []

	for pivot in congested_pivots:
		if next_pivot := get_next(congested_pivots, pivot):
			next_gap = next_pivot["low"] - pivot["low"]
			if next_gap >= spacing:
				decongested_pivots.append(pivot)
				decongested_pivots.append(next_pivot)

			else:
				strong_pivot, weak_pivot = get_stronger_low(range, pivot, next_pivot)
				decongested_pivots.append(strong_pivot)
				# print(strong_pivot)
				try:
					congested_pivots.remove(weak_pivot)
				except ValueError:
					pass
		else:
			decongested_pivots.append(pivot)
	return decongested_pivots


def decongest_highs(range, gap, congested_pivots):
	"""
	find and return the strongest pivot levels when pivots are closely positions to each other
	The strongest pivots with the highest previous swing highs
	"""
	range_high, range_low = pivots.define_range(range)
	range_height = range_high["high"] - range_low["low"]
	spacing = range_height * gap / 100

	decongested_pivots = []

	for pivot in congested_pivots:
		if next_pivot := get_next(congested_pivots, pivot):
			next_gap = pivot["high"] - next_pivot["high"]
			if next_gap >= spacing:
				decongested_pivots.append(pivot)
				decongested_pivots.append(next_pivot)

			else:
				strong_pivot, weak_pivot = get_stronger_high(range, pivot, next_pivot)
				decongested_pivots.append(strong_pivot)
				try:
					decongested_pivots.remove(weak_pivot)
				except ValueError:
					pass
		else:
			decongested_pivots.append(pivot)
	return decongested_pivots


def previous_swing_high(range, pivot_candle):
    """
    Find the swing high for a given pivot candle by examining previous prices.

    Parameters:
    candles (list of dict): List of candlestick data.
    pivot_candle (dict): The pivot candle to find the swing high for.

    Returns:
    float: The swing high price.
    """
    pivot_index = range.index(pivot_candle)
    for candle in reversed(range[:pivot_index]):
        if candle["low"] < pivot_candle["low"]:
            return max(c["high"] for c in range[range.index(candle) + 1:pivot_index])
    return max(c["high"] for c in range[:pivot_index])


def previous_swing_low(range, pivot_candle):
    """
    Find the swing high for a given pivot candle by examining previous prices.

    Parameters:
    candles (list of dict): List of candlestick data.
    pivot_candle (dict): The pivot candle to find the swing high for.

    Returns:
    float: The swing high price.
    """
    pivot_index = range.index(pivot_candle)
    for candle in reversed(range[:pivot_index]):
        if candle["high"] > pivot_candle["high"]:
            return min(c["low"] for c in range[range.index(candle) + 1:pivot_index])
    return min(c["low"] for c in range[:pivot_index])


def get_stronger_low(range, candle1, candle2):
	"""
	Compare the strength of two pivot point candles and return the strongest candle.

	Parameters:
	candles (list of dict): List of candlestick data.
	candle1 (dict): The first pivot candle.
	candle2 (dict): The second pivot candle.

	Returns:
	dict: The strongest pivot candle.
	"""

	swing_high1 = previous_swing_high(range, candle1)
	swing_high2 = previous_swing_high(range, candle2)

	swing1 = swing_high1 - candle1["low"]
	swing2 = swing_high2 - candle2["low"]

	if swing1 >= swing2:
		return candle1, candle2
	else:
		return candle2, candle1

def get_stronger_high(range, candle1, candle2):
	"""
	Compare the strength of two pivot point candles and return the strongest candle.

	Parameters:
	candles (list of dict): List of candlestick data.
	candle1 (dict): The first pivot candle.
	candle2 (dict): The second pivot candle.

	Returns:
	dict: The strongest pivot candle.
	"""

	swing_low1 = previous_swing_low(range, candle1)
	swing_low2 = previous_swing_low(range, candle2)

	swing1 = candle1["high"] - swing_low1
	swing2 = candle2["high"] - swing_low2

	if swing1 >= swing2:
		return candle1, candle2
	else:
		return candle2, candle1


def get_next(lst, current_element):
    """
    Get the next element in the list using the current element.

    Parameters:
    lst (list): The list of elements.
    current_element: The current element to find the next element for.

    Returns:
    The next element in the list, or None if the current element is the last one.
    """
    try:
        current_index = lst.index(current_element)
        if current_index < len(lst) - 1:
            return lst[current_index + 1]
        else:
            return None  # Current element is the last one
    except ValueError:
        return None  # Current element not found in the list



def get_previous(range, current_element):
    """
    Get the previous element in the list using the current element.

    Parameters:
    lst (list): The list of elements.
    current_element: The current element to find the next element for.

    Returns:
    The next element in the list, or None if the current element is the last one.
    """
    try:
        current_index = range.index(current_element)
        if current_index > 0:
            return range[current_index - 1]
        else:
            return None  # Current element is the last one
    except ValueError:
        return None  # Current element not found in the list


