from typing import Literal
from pydantic import BaseModel, Field

class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: float

class Tp(BaseModel):
    target: float
    status: Literal['pending', 'success', 'failed']


class SignalData(BaseModel):
    symbol: str
    interval: str
    time: int
    signal_type: str
    entry_price: float
    sl: float
    tp1: float
    tp2: float
    tp1_status: Literal['pending', 'success', 'failed']
    tp2_status: Literal['pending', 'success', 'failed']
    status: Literal['pending', 'partial', 'success', 'failed']

# for the SignalData.status
# failed: when no take profit target is hit before stop loss is hit
# pending: when no take profit target is hit and stop loss has not been hit
# partial: some take profit targets are hit but not all
#
# for tp status
# pending: tp target not hit but stop loss not hit either
# success: tp target hit before stop loss is hit
# failed: stop loss hit before tp target hit


class SignalModel(BaseModel):
    id: str = Field(alias='$id')
    data: SignalData

