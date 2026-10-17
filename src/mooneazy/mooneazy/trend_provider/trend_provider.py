from ..candles_api.candles_api import api
from .trend_from_emas import get_trend_from_emas 
from ..models.scalping_configs import ScalpingAnalysisConfigs 
from ..ultimate_setups.ultimate_setups.core import pivots
from ..models.candles import Candle 

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


def touches(candle, level):
    return float(candle['high']) > float(level) > float(candle['low'])


def get_trend_from_sr(support_pivot:Candle, resistance_pivot:Candle, current_candle:Candle):
    sh = support_pivot.get('close')
    sl = support_pivot.get('low')
    rh = resistance_pivot.get('high')
    rl = resistance_pivot.get('close')
    cc = current_candle

    if sl and cc['close'] > sl and (
        touches(cc, sh) or touches(cc, sl) or (sh > cc['close'] > sl)
    ):
        return 'buy'
    if rl and cc['close'] > rl and (
        touches(cc, rh) or touches(cc, rl) or (rh > cc['close'] > rl)
    ):
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
        self._sr_pivots = sr_pivots
        self._ema_periods = self._configs.ema_cross_periods
        self._pivot_lookback = self._configs.sr_pivot_lookback 
        self._candles = self.fetch_candles()

    def get_current_candle(self):
        return get_candles(
            symbol=self._symbol, 
            interval=self._configs.default_interval, 
            limit=2
        )[-1]

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

        return support_pivots[-1], resistance_pivots[-1]

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
        current_candle = self.get_current_candle()
        return get_trend_from_sr(support_pivot, resistance_pivot, current_candle)

    def get_trend(self):
        return self.get_trend_from_sr() or self.get_trend_from_emas()


