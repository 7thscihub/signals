from pydantic import BaseModel, Field

class Coin(BaseModel):
    name: str 
    symbol: str 
    can_dca: bool 
    can_swing: bool 
    can_scalp: bool 
    dca_intervals: list[str] = Field(default_factory=list)
    scalping_intervals: list[str] = Field(default_factory=list)
    swing_intervals: list[str] = Field(default_factory=list)


class AltCoin(Coin):
    can_scalp: bool = False 
    can_swing: bool = True 
    can_dca: bool = True 
    dca_intervals: list[str] = ['3d', '1w']
    swing_intervals: list[str] = ['8h', '1d']


class LargeCap(Coin):
    can_dca: bool = True 
    can_swing: bool = True
    can_scalp: bool = True
    dca_intervals: list[str] = ['1d', '3d']
    scalping_intervals: list[str] = ['15m', '30m']
    swing_intervals: list[str] = ['4h', '8h', '12h']




