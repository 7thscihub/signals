from typing import Callable
from pydantic import validate_call
from ..candles_api.candles_api import api as candles_api
from ..pullback_strategy.pullback_strategy import signals as pullback_signals
from ..pullback_strategy.pullback_strategy.head_and_shoulder import HeadAndShoulder
from ..breakout_strategy.breakout_strategy import breakouts
from ..ultimate_setups.ultimate_setups import signals as ult_signals
from ..trend_provider.trend_provider import TrendProvider
from .config import Configs
from . import htf_trend
from . import util
from ..validators.scalping_configs import ScalpingAnalysisConfigs, ScalpingStrategiesIntervals 


class Analyze:
    def __init__(self, 
                 symbol, interval, candles, trend, configs:ScalpingAnalysisConfigs=ScalpingAnalysisConfigs()
        ):
        self._symbol = symbol
        self._interval = interval 
        self._configs = configs
        self._candles = candles
        self._trend =  trend
    
    def get_pullback_signal(self)->dict[str, any] | None:
        signals = pullback_signals.get_trade_signal(
            candles = self._candles,
            interval = self._interval,
            configs=self._configs.pullback_configs,
            trend=self._trend,
        )
        return signals
    
    def get_breakout_signals(self):
        signals = []
        signal = breakouts.Breakouts(
            candles=self._candles, 
            interval=self._interval, 
            configs=self._configs.breakout_configs,
            trend=self._trend 
        ).get_latest_trade_signal()
        if signal:
            signals.append(signal)
        return signals 

    def get_ult_signal(self):
        signals = []
        signal = ult_signals.get_ult_signal(
            candles=self._candles,
            configs=self._configs.ultimate_setups_configs, 
            interval=self._interval
        )
        if signal:
            signals.append(signal)
        return signals

    def get_hs_signal(self):
        signals = []
        trade_signals = HeadAndShoulder(
            candles=self._candles, 
            interval=self._interval,
            configs=self._configs.heads_and_shoulders_configs
        ).latest_trade_signals()
        if trade_signals:
            signals.extend(trade_signals)
        return signals

    def get_signals(self, strategy_intervals:dict[str, list]):
        strategies = {
            'breakout': self.get_breakout_signals,
            'pullback': self.get_pullback_signal,
            'ult_setups': self.get_ult_signal,
            'heads_and_shoulders': self.get_hs_signal
        }
        all_signals = []
        for key, value in strategy_intervals.items():
            if not self._interval in value:
                continue
            if signals:= strategies[key]():
                all_signals.extend(signals)
        for signal in all_signals:
            signal['utc_time'] = util.unix_to_utc(signal['trigger_candle']['time'])
            
        return all_signals


def get_candles(symbol, interval, limit):
    parameters = {
        'symbol': symbol,
        'limit': limit,
        'interval': interval
    }
    return candles_api.get_candles(parameters)


@validate_call 
def get_symbol_signals(
        symbol:str, 
        configs, 
        trend:str='', 
        strategy_intervals=dict[str, list]
    ):
    symbol_signals = []
    intervals_list = []
    for intervals in strategy_intervals.values():
        intervals_list.extend(intervals)

    unique_intervals = set(intervals_list)
    for interval in unique_intervals:
        candles = get_candles(
            symbol, interval=interval, limit=configs.default_limit
        )
        signals = Analyze(
            symbol=symbol, 
            interval=interval, 
            candles=candles, 
            configs=configs, 
            trend=trend
        ).get_signals(strategy_intervals=strategy_intervals)
        if signals:
            symbol_signals.extend(signals)

    return symbol_signals 



@validate_call
def get_scalping_signals(
        symbols:list[str]=ScalpingAnalysisConfigs().supported_symbols,
        configs: ScalpingAnalysisConfigs = ScalpingAnalysisConfigs(),
        trend_provider:Callable=TrendProvider,
        strategy_intervals: ScalpingStrategiesIntervals = ScalpingStrategiesIntervals()
    ):
    scalping_signals = []
    strategy_intervals_dict = strategy_intervals.model_dump()
    trend_intervals = configs.scalping_trend_intervals
    for symbol in symbols:
        trend = trend_provider(symbol, intervals=trend_intervals).get_trend()
        symbol_signals = get_symbol_signals(symbol, configs, trend, strategy_intervals_dict)
        scalping_signals.extend(symbol_signals)

    return scalping_signals






