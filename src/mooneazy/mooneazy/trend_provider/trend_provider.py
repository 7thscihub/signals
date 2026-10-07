from ..breakout_strategy.breakout_strategy import errors
from ..candles_api.candles_api import api
from .trend_from_emas import get_trend_from_emas 


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


def get_in_trend_signals(signals:list[dict], symbol: str, trend_intervals:list[str]=[], trend:str=''):
    if not trend_intervals and not trend:
        raise ValueError('Provide Trend direction or trend intervals for generating trends')
    symbol_trend = trend or get_trend(symbol=symbol, interval=trend_intervals)
    in_trendrend_signals = []
    for signal in signals:
        if signal['direction'] == symbol_trend:
            in_trendrend_signals.append(signal)
    return in_trendrend_signals


class TrendProvider:
    def __init__(self, symbol, intervals, emas_periods=(8, 20)):
        self._symbol = symbol
        self._intervals = intervals

    def get_trend(self):
        return get_trend_from_htf_emas(
            symbol=self._symbol, intervals=self._intervals
        )

    
