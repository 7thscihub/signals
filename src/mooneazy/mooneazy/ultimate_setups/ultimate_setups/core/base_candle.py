from . import settings


class Candle(dict):
	def __init__(self, candle_data):
		super().__init__(candle_data)
		self._candle = candle_data
		self._fib = 0.236
	
	@property
	def pinbar_fib(self):
		if not self._fib:
			raise AttributeError(
				"The candle property Pinbar fib needs to be set first"
			)
		return self._fib

	@pinbar_fib.setter
	def pinbar_fib(self, pinbar_fib):
		self._fib = pinbar_fib

	def body_size(self):
		"""
		red candles will have negative bodies
		"""
		return self["close"] - self["open"]

	def size(self):
		"""
		red candles will have negative sizes
		"""
		return self["high"] - self["low"]

	def mid_body(self):
		return self.body_size() / 2 + self["open"]

	def is_bullish(self):
		return self["close"] > self["open"]

	def is_bearish(self):
		return self["open"] > self["close"]

	def is_shooting_star(self):
		return self["low"] + self._fib * self.size() > max(self["open"], self["close"])

	def is_hammer(self):
		return self["high"] - (self._fib * self.size()) < min(self["open"], self["close"])

	def is_green_pinbar(self):
		return self.is_bullish() and self.is_hammer()

	def is_red_pinbar(self):
		return self.is_shooting_star() and self.is_bearish()

	def is_strong_breakout(self, level):
		return (self.body_size() / 2) + self["open"] > level > self["low"]

	def is_strong_breakdown(self, level):
		return self["open"] - (self.body_size() / 2) < level

	def candle_index(self, candles):
		try:
			return candles.index(self)
		except ValueError:
			raise ValueError(f"candle mot in the candles")



