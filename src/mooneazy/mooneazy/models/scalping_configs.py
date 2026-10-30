from typing import Literal 
from pydantic import BaseModel, ConfigDict 


class ScalpingStrategiesIntervals(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    pullback: list[str] = ['15m']
    breakout: list[str] = ['15m', '30m']
    heads_and_shoulders: list[str] = ['30m']
    ult_setups: list[str] = ['30m', '4h']


class UltimateSetupsConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)   

    fo_lookback: int = 5 
    pivot_lookback: int = 30
    tp_rrrs: tuple[float, float] = (1.5, 3)
    sl_padding: float = 0.001
    ult_setups_intervals: list = ['30m', '4h']
    levels_interval: str = '4h'
    levels_pivot_lookback: int = 5
    levels_limit: int = 200


class BreakoutConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fo_lookback: int = 5
    ema_cross_periods: tuple[int, int] = (8, 20)
    hull_period: int = 55
    min_opposite_candles: int = 2 
    min_score: int = 8
    tp_rrrs: tuple = (2, 5)
    breakout_intervals: list = ['30m', '15m']
    trend: Literal['buy', 'sell', ''] = ''
    sl_padding: float = 0.001


class PullbackConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    pullback_lookback_values: tuple[int, int] = (5, 15)
    fo_lookback: int = 3
    min_fib: float = 0.382
    max_fib: float = 0.7
    tp_rrrs: tuple[float, float] = (2, 5)
    sl_padding: float = 0.001
    range_lookback: int = 110
    min_follow_up_retracement_fib: float = 0.7
    pullback_intervals:list = ['15m']

class HeadsAndShouldersConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pivot_lookback:int = 5 
    fo_lookback:int = 3 
    tp_rrrs:tuple = (2, 5)
    sl_padding: str = 0.001
    sr_fib: float = 0.8
    heads_and_shoulders_intervals:list = ['30m']

class ScalpingAnalysisConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
     
    sr_pivot_lookback: int = 30
    sr_limit: int = 230
    sr_interval: str = '4h'

    supported_symbols:list = ['ETHUSDT', 'BTCUSDT', 'XAUUSDT']
    default_limit:int = 500
    ema_cross_periods:tuple = (8, 20)
    default_interval: str = '30m'
    default_fo_lookback: int = 5
    
    levels_interval:str = '4h'
    levels_limit: int = 20
    levels_pivot_lookback: int = 5
    
    strategy_intervals: dict = {
        'breakout': ['15m', '30m',],
        'ult_setups': ['30m', '4h'],
        'pullback': ['15m'],
        'heads_and_shoulders': ['30m']
    }

    ema_trend_intervals: list = ['1d']
    ema_trend_limit: int = 200
    ema_trend_periods: tuple = (8, 20)

    heads_and_shoulders_configs: HeadsAndShouldersConfigs = HeadsAndShouldersConfigs()
    pullback_configs: PullbackConfigs = PullbackConfigs()
    breakout_configs: BreakoutConfigs = BreakoutConfigs()
    ultimate_setups_configs: UltimateSetupsConfigs = UltimateSetupsConfigs()
    
