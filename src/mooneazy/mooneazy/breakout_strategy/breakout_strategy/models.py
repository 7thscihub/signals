from typing import Literal 
from pydantic import BaseModel, ConfigDict


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


class EmaModel(BaseModel):
    time: int
    value: float


