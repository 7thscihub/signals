from ..candles_api.candles_api import api
from .trend_from_emas import get_trend_from_emas 
from ..models.scalping_configs import ScalpingAnalysisConfigs 
from ..ultimate_setups.ultimate_setups.core import pivots 
from ..models.candles import Candle 
from ..pullback_strategy.pullback_strategy import util


def get_candles(symbol, interval, limit=200):
    parameters = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit 
    }
    candles = api.get_candles(parameters)
    # print(f"len candles: {len(candles)}")
    return candles


def get_trend_from_htf_emas(symbol, intervals: list = ['4h', '1d', '1w'], ema_periods=(8, 20)) -> str | None:
    trends = []
    for interval in intervals:
        candles = get_candles(symbol=symbol, interval=interval)
        trends.append(get_trend_from_emas(candles, ema_periods=ema_periods))
    for trend in trends:
        if trends.count('buy') >= len(trends) * 0.65:
            return 'buy'
        if trends.count('sell') >= len(trends) * 0.65:
            return 'sell'
    return None


def get_current_candle(symbol, inerval='4h'):
    return get_candles(symbol=symbol, interval='1m', limit=2)[-1]


def get_sr_pivots(candles, pivot_lookback):
    support_pivot, resistance_pivot = {}, {}
    support_pivots = pivots.get_lows(candles, pivot_lookback)
    if support_pivots:
        support_pivot = support_pivots[-1]
    resistance_pivots = pivots.get_highs(candles, pivot_lookback)
    if resistance_pivots:
        resistance_pivot = resistance_pivots[-1]
    return support_pivot, resistance_pivot


def get_levels(symbol, configs):
    candles = get_candles(symbol, configs.levels_interval, configs.levels_limit)
    pivot_lookback = configs.levels_pivot_lookback
    support_pivot, resistance_pivot = get_sr_pivots(candles, pivot_lookback)

    levels = {'buy_levels': [], 'sell_levels': [] }

    if support_pivot:
        buy_level = {
            'time': support_pivot.get('time'), 
            'value': support_pivot.get('low')
        }
        levels['buy_levels'].append(buy_level)

    if resistance_pivot:
        sell_level = {
            'time': resistance_pivot.get('time'),
            'value': resistance_pivot.get('high')
        }
        levels['sell_levels'].append(sell_level)

    return levels 


def touches(candle, level):
    return float(candle['high']) > float(level) > float(candle['low'])


def get_support_high(pivot_candle):
    if not pivot_candle:
        return None 
    return min(pivot_candle.get('close'), pivot_candle.get('open'))


def get_resistance_low(pivot_candle):
    if not pivot_candle:
        return None
    return max(pivot_candle.get('close'), pivot_candle.get('open'))

def is_on_sr(candle, sr_high, sr_low, direction):
    if candle['close'] > sr_high and direction == 'sell':
        return False 
    if candle['close'] < sr_low and direction == 'buy':
        return False
    return True 


def get_trend_from_sr(support_pivot:Candle, resistance_pivot:Candle, current_candles:list[Candle]):
    sh = get_support_high(support_pivot)
    sl = support_pivot.get('low')
    rh = resistance_pivot.get('high')
    rl = get_resistance_low(resistance_pivot)
    currenct_candle = current_candles[-1]
    highest_candle = max(current_candles, key=lambda candle:candle['high'])
    lowest_candle = min(current_candles, key=lambda candle:candle['low'])
    # print(f"sh: {sh}, lc_l: {lowest_candle['low']}, lc_t: {util.unix_to_utc(lowest_candle['time'])}")
    if sl and currenct_candle['close'] > sl and (
        touches(lowest_candle, sh) or touches(lowest_candle, sl) or (sh > currenct_candle['close'] > sl)
    ):
        return 'buy'
    if rl and currenct_candle['close'] > rl and (
        touches(highest_candle, rh) or touches(highest_candle, rl) or (rh > currenct_candle['close'] > rl)
    ):
        return 'sell'
    return None 


class TrendProvider:
    def __init__(self, 
        symbol, 
        configs=ScalpingAnalysisConfigs(), 
        sr_levels:dict[str, list[dict]] = [],
        current_candles: list[dict] = [],
        sr_candles:list[dict] = [],
        ema_trends_candles: list[list[dict]] = []
    ):
        self._symbol = symbol
        self._configs = configs
        self._ema_intervals = self._configs.ema_trend_intervals
        self._sr_levels = sr_levels
        self._sr_interval = self._configs.sr_interval
        self._ema_periods = self._configs.ema_trend_periods
        self._pivot_lookback = self._configs.sr_pivot_lookback 
        self._ema_candles = ema_trends_candles or self.fetch_ema_candles()
        self._sr_candles = self.fetch_sr_candles()
        self._current_candles = current_candles or self.get_current_candles()

    def get_current_candles(self):
        candles = get_candles(
            symbol=self._symbol, 
            interval=self._configs.default_interval, 
            limit=self._configs.default_fo_lookback 
        )
        return candles

    def fetch_ema_candles(self):
        candles: list[list[dict]] = []
        limit = self._configs.ema_trend_limit 
        for interval in self._ema_intervals:
            interval_candles = get_candles(self._symbol, interval, limit)
            candles.append(interval_candles)
        return candles
 
    def fetch_sr_candles(self):
        limit = self._configs.sr_limit
        print(f"sr: {self._symbol}, {self._sr_interval}, {limit}")
        return get_candles(self._symbol, self._sr_interval, limit)

    def get_sr_pivots(self):
        candles = self._sr_candles
        sr_pivots = get_sr_pivots(candles, self._pivot_lookback)
        # print(f"sr_pivots: {sr_pivots}")
        return sr_pivots

    def get_levels(self):
        if self._sr_levels:
            return self._sr_levels
        support_pivot, resistance_pivot = self.get_sr_pivots()
        buy_level = { 
            'time': support_pivot['time'], 'value': support_pivot['low'] 
        }
        sell_level = { 
            'time': resistance_pivot['time'], 'value': resistance_pivot['high'] 
        }
        return {
            "buy_levels": [buy_level],
            "sell_levels": [sell_level]
        }

    def get_trend_from_emas(self, threshold=0.65):
        trends = []
        for candles in self._ema_candles:
            trends.append(get_trend_from_emas(candles, ema_periods=self._ema_periods))
        for trend in trends:
            if trends.count('buy') >= len(trends) * threshold:
                return 'buy'
            if trends.count('sell') >= len(trends) * threshold:
                return 'sell'
        return None

    def get_trend_from_sr(self):
        support_pivot, resistance_pivot = self.get_sr_pivots()
        current_candles = self._current_candles
        return get_trend_from_sr(support_pivot, resistance_pivot, current_candles)

    def get_trend(self):
        return self.get_trend_from_sr() or self.get_trend_from_emas()


def get_trend(symbol, configs):
    trend = TrendProvider(symbol=symbol, configs=configs).get_trend_from_sr()
    return trend


if __name__ == "__main__":
    symbol = "XAUUSDT"
    configs = ScalpingAnalysisConfigs()
    print(get_trend(symbol, configs))



