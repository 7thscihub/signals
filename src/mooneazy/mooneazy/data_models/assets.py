from typing import Literal, Optional
from pydantic import Basemodel


class Asset(Basemodel):
    name: str 
    symbol: str 
    can_dca: bool 
    can_swing: bool 
    can_scalp: bool 
    dca_intervals: list[str] = []
    scalping_intervals: list[str] = []
    swing_intervals: list[str] = []


class AltCoin(Asset):
    can_scalp = False 
    can_swing = True 
    can_dca = True 
    dca_intervals = ['3d', '1w']
    swing_intervals = ['8h', '1d']





