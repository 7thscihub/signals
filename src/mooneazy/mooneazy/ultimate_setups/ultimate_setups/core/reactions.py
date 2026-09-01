
class BreakOut:
	"""
	checks if the last candle in the given candles is a breakout.
	
	parameter:
	candles: List[dict] should exclude unclosed candles from the API call
	the number of candles should be more than the lookback value
	"""

	def __init__(self, candles, lookback, min_opposite_candles):
		self.candles = candles
		self.lookback_candles = self.candles[-lookback - 1:-1]
		self._breakout_candle = self.candles[-1]
		self.min_opposite_candles = min_opposite_candles

	@property
	def breakout_candle(self):
		return self._breakout_candle

	def set_min_opposite_candles(self, value):
		self.min_opposite_candles = value

	def get_lookback_low(self):
		return min(c["low"] for c in self.lookback_candles)

	def get_lookback_high(self):
		return max(c["high"] for c in self.lookback_candles)

	def count_red(self):
		"""
		checks whether there are enoough red candles within the range
		"""
		count = 0
		for candle in self.lookback_candles:
			if candle["close"] < candle["open"]:
				count += 1
		return count >= self.min_opposite_candles

	def count_green(self):
		"""
		checks whether there are enoough green candles within the range
		"""
		count = 0
		for candle in self.lookback_candles:
			if candle["close"] > candle["open"]:
				count += 1
		return count >= self.min_opposite_candles

	def is_weak_bullish(self):
		if not self.count_red():
			return False

		# excluding the trigger candle
		candle = self.breakout_candle
		lookback_high = self.get_lookback_high()
		lookback_max_close = max(c["close"] for c in self.lookback_candles)

		# checking for breakout
		return candle["high"] > lookback_high > candle["close"] > lookback_max_close

	def is_strong_bullish(self):
		if not self.count_red():
			return False

		candle = self.breakout_candle
		lookback_high = self.get_lookback_high()

		return candle["close"] > lookback_high

	def is_weak_bearish(self):
		if not self.count_green():
			return False

		candle = self.breakout_candle
		lookback_low = self.get_lookback_low()
		lookback_min_close = min(c["close"] for c in self.lookback_candles)

		return candle["low"] < lookback_low < candle["close"] < lookback_min_close

	def is_strong_bearish(self):
		if not self.count_green():
			return False

		candle = self.breakout_candle
		lookback_low = self.get_lookback_low()

		return candle["close"] < lookback_low

	def is_bullish(self):
		return self.is_strong_bullish() or self.is_weak_bullish()

	def is_bearish(self):
		return self.is_strong_bearish() or self.is_weak_bearish()

	def is_big_candle(self):
		lookback_height = self.get_lookback_high() - self.get_lookback_low()
		candle_height = abs(self.breakout_candle["close"] - self.breakout_candle["open"])

		return candle_height > lookback_height


class EngulfingBreakout(BreakOut):
	def __init__(self, candles, lookback, min_opposite):
		super().__init__(candles, lookback, min_opposite)

	def get_lookback_range(self):
		lookback_high = max(c["high"] for c in self.lookback_candles)
		lookback_low = min(c["low"] for c in self.lookback_candles)
		return lookback_high, lookback_low

	def lookback_mid(self):
		high, low = self.get_lookback_range()
		return low + (high - low) / 2

	def get_bullish_breakout(self):
		if self.is_strong_bullish() and self.breakout_candle["low"] <= self.lookback_mid():
			return self.breakout_candle
		return None

	def get_bearish_breakout(self):
		if self.is_strong_bearish() and self.breakout_candle["high"] >= self.lookback_mid():
			return self.breakout_candle
		return None


class LevelBreakout:
	"""
	assumes that the candles argument excludes the active still-open candle from exchanges
	"""

	def __init__(self, candles, level, lookback):
		self.lookback = lookback
		self.lookback_candles = candles[-lookback - 1:-1]
		self.breakout_candle = candles[-1]
		self.level = level

	def is_bullish(self):
		"""
		checks if atleast half of the candle body is above a level
		"""
		level = self.level
		candle = self.breakout_candle
		mid_body = self.get_mid_body(candle)
		return max(c["close"] for c in self.lookback_candles) <= level < mid_body

	def is_bearish(self):
		"""
		checks if at least half of the candle body is above a level
		"""
		level = self.level
		candle = self.breakout_candle
		mid_body = self.get_mid_body(candle)
		return min(c["close"] for c in self.lookback_candles) >= level > mid_body

	def get_mid_body(self, candle):
		return (candle["close"] - candle["open"]) / 2 + candle["open"]


if __name__ == "__main__":
	...
