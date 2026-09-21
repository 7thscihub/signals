from pydantic import BaseModel, Field
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
    time: int
    entry_price: float
    symbol: str
    sl: float
    tp1: float
    tp2: float
    direction: str
    interval: str 
    signal_type: str
    tp1_status: Literal['sucess', 'pending', 'failed']
    tp1_status: Literal['sucess', 'pending', 'failed']
    status: Literal['sucess', 'pending', 'failed']


class SignalModel(BaseModel):
    id: str = Field(alias='$id')
    data: SignalData


class ResultData(BaseModel):
    id: str
    tp1_status: Literal['sucess', 'pending', 'failed']
    tp1_status: Literal['sucess', 'pending', 'failed']


class ResultModel(BaseModel):
    id: str
    data: ResultData




