from pydantic import BaseModel, Field, AliasChoices
from typing import Literal

class TriggerCandle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: int


class SignalData(BaseModel):
    symbol: str
    interval: str
    time: int
    utc_time: str
    direction: str
    signal_type: str
    entry_price: float
    sl: float
    tp1: float
    tp2: float
    tp1_status: Literal['pending', 'success', 'failed'] = 'pending'
    tp2_status: Literal['pending', 'success', 'failed'] = 'pending'
    status: Literal["pending", "closed"] = 'pending'


class SignalModel(BaseModel):
    id: str = Field(validation_alias=AliasChoices('$id', 'id'))
    data: SignalData


class ResultData(BaseModel):
    id: str
    tp1_status: Literal['sucess', 'pending', 'failed']
    tp1_status: Literal['sucess', 'pending', 'failed']


class ResultModel(BaseModel):
    id: str
    data: ResultData




