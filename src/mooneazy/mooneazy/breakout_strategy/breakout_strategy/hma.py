import math


def calculate_wma(data, period):
    """Calculates the Weighted Moving Average (WMA) for a list of data.

    Returns a list of the same length, with None for indices without enough data.
    """
    wma_result = [None] * len(data)
    if period < 1 or len(data) < period:
        return wma_result

    # Sum of weights: 1 + 2 + ... + period
    denominator = (period * (period + 1)) // 2

    for i in range(period - 1, len(data)):
        window = data[i - period + 1 : i + 1]

        # Calculate the weighted sum
        numerator = sum((j + 1) * val for j, val in enumerate(window))
        wma_result[i] = numerator / denominator

    return wma_result


def calculate_hma(data, period):
    """Calculates the Hull Moving Average (HMA) without external dependencies.

    :param data: list of floats/ints (e.g., closing prices)
    :param period: int, the lookback period
    :return: list of HMA values (padded with None where unavailable)
    """
    if period < 2:
        raise ValueError("Period must be 2 or greater.")

    length = len(data)

    # 1. Calculate WMA for half the period and full period
    half_period = int(period / 2)
    wma_half = calculate_wma(data, half_period)
    wma_full = calculate_wma(data, period)

    # 2. Calculate the raw HMA: (2 * WMA_half) - WMA_full
    # We can only calculate this where both WMA values are not None
    raw_hma = [None] * length
    for i in range(length):
        if wma_half[i] is not None and wma_full[i] is not None:
            raw_hma[i] = (2 * wma_half[i]) - wma_full[i]

    # 3. Smooth raw_hma with a WMA of the square root of the period
    hma_period = int(math.sqrt(period))

    # Because raw_hma contains leading 'None' values, we extract the valid sub-list,
    # run WMA on it, and then map it back to the original list positions.
    first_valid_idx = next(
        (i for i, val in enumerate(raw_hma) if val is not None), None
    )

    if first_valid_idx is None:
        return [None] * length

    valid_raw_hma = raw_hma[first_valid_idx:]
    smoothed_valid = calculate_wma(valid_raw_hma, hma_period)

    # Reconstruct the final list with proper padding
    hma_result = [None] * first_valid_idx + smoothed_valid

    return hma_result


class BreakoutHMA:
    """
    Returns the last n hma values for the breakout strategy
    Which has a length similar to the lookback_left parameter
    """
    def __init__(self, indicator_candles, period=55, lookback_left=5):
        self.indicator_candles = indicator_candles
        self.period = period
        self.lookback_left = lookback_left

    def values(self) -> list[int | None]:
        close = [candle['close'] for candle in self.indicator_candles]
        all_hma = calculate_hma(data=close, period=self.period)
        return all_hma[-self.lookback_left:]

    def get_all_hmas(self) -> list[int | None]:
        close = [candle['close'] for candle in self.indicator_candles]
        all_hma = calculate_hma(data=close, period=self.period)
        return all_hma
