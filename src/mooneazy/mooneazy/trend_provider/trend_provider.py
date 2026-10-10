from ..candles_api.candles_api import api
from .trend_from_emas import get_trend_from_emas 
from ..models.scalping_configs import ScalpingAnalysisConfigs 
from ..ultimate_setups.ultimate_setups.core import pivots


def get_candles(symbol, interval, limit=200):
    parameters = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit 
    }
    return api.get_candles(parameters)


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


def get_current_price(symbol):
    latest_candle = get_candles(symbol=symbol, interval='1m', limit=2)[-1]
    return latest_candle['close']


def get_sr_pivots(candles, pivot_lookback):
    support_pivot = pivots.get_lows(candles, pivot_lookback)[-1]
    resistance_pivot = pivots.get_highs(candles, pivot_lookback)[-1]
    return support_pivot, resistance_pivot


def get_trend_from_sr(support_pivot, resistance_pivot, current_price):
    if support_pivot['close'] >= current_price >= support_pivot['low']:
        return 'buy'
    if resistance_pivot['close'] >= current_price >= resistance_pivot['high']:
        return 'sell'
    return None 


class TrendProvider:
    def __init__(self, 
        symbol, 
        configs=ScalpingAnalysisConfigs(), 
        sr_pivots=None, 
        current_price=None
    ):
        self._symbol = symbol
        self._configs = configs
        self._intervals = self._configs.scalping_trend_intervals
        self._current_price = current_price or get_current_price(symbol=symbol)
        self._sr_pivots = sr_pivots
        self._ema_periods = self._configs.ema_cross_periods
        self._pivot_lookback = self._configs.sr_pivot_lookback 
        self._candles = self.fetch_candles()

    def fetch_candles(self):
        candles: list[list[dict]] = []
        for interval in self._intervals:
            candles.append(get_candles(self._symbol, interval))
        return candles

    def get_sr_pivots(self):
        if self._sr_pivots:
            return self._sr_pivots
            
        support_pivots = []
        resistance_pivots = []
        for candles in self._candles:
            sp, rp = get_sr_pivots(candles, self._pivot_lookback)
            support_pivots.append(sp)
            resistance_pivots.append(rp)

        sorted_support_pivots = sorted(support_pivots, key=lambda k: k['time'])
        sorted_resistance_pivots = sorted(resistance_pivots, key=lambda k: k['time'])
        return sorted_support_pivots[-1], sorted_resistance_pivots[-1]

    def get_trend_from_emas(self):
        trends = []
        for candles in self._candles:
            trends.append(get_trend_from_emas(candles, ema_periods=self._ema_periods))
        for trend in trends:
            if trends.count('buy') >= len(trends) * 0.65:
                return 'buy'
            if trends.count('sell') >= len(trends) * 0.65:
                return 'sell'
        return None

    def get_trend_from_sr(self):
        support_pivot, resistance_pivot = self.get_sr_pivots()
        current_price = self._current_price
        return get_trend_from_sr(support_pivot, resistance_pivot, current_price)

    def get_trend(self):
        return self.get_trend_from_sr() or self.get_trend_from_emas()


