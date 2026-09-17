from pydantic import BaseModel

class TriggerCandle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: int


class SignalModel(BaseModel):
    time: int
    entry_price: float
    symbol: str
    sl: float
    tp1: float
    tp2: float
    direction: str
    interval: str 
    signal_type: str


