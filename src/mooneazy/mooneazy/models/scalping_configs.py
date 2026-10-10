from typing import Literal 
from pydantic import BaseModel, ConfigDict 


class ScalpingStrategiesIntervals(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    pullback: list[str] = ['15m']
    breakout: list[str] = ['15m', '30m']
    heads_and_shoulders: list[str] = ['30m']
    ult_setups: list[str] = ['30m']


class UltimateSetupsConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)   

    fo_lookback: int = 5 
    pivot_lookback: int = 30
    tp_rrrs: tuple[float, float] = (1.5, 3)
    sl_padding: float = 0.001


class BreakoutConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fo_lookback: int = 5
    ema_cross_periods: tuple[int, int] = (8, 20)
    hull_period: int = 55
    min_opposite_candles: int = 2 
    min_score: int = 5
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
    

class HeadsAndShouldersConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pivot_lookback:int = 5 
    fo_lookback:int = 3 
    tp_rrrs:tuple = (2, 5)
    sl_padding: str = 0.001
    sr_fib: float = 0.8


class ScalpingAnalysisConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    sr_pivot_lookback: int = 30
    supported_symbols:list = ['BTCUSDT','XAUUSDT', 'BTCUSDT']
    default_limit:int = 1500
    ema_cross_periods:tuple = (8, 20)

    strategy_intervals: dict = {
        'breakout': ['15m', '30m',],
        'ult_setups': ['30m'],
        'pullback': ['15m'],
        'heads_and_shoulders': ['30m']
    }

    scalping_trend_intervals: list = ['4h']
    heads_and_shoulders_configs: HeadsAndShouldersConfigs = HeadsAndShouldersConfigs()
    pullback_configs: PullbackConfigs = PullbackConfigs()
    breakout_configs: BreakoutConfigs = BreakoutConfigs()
    ultimate_setups_configs: UltimateSetupsConfigs = UltimateSetupsConfigs()

