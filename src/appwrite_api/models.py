from pydantic import BaseModel
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
    tp1_results: str
    tp1_results: str
    is_open: bool


class SignalModel(BaseModel):
    id: str = Field(Valifation_aliase='$id')
    data: SignalData


class ResultData(BaseModel):
    tp1_results: Literal['sucess', 'pending', 'failed']
    tp2_results: Literal['sucess', 'pending', 'failed']


class ResultModel(BaseModel):
    id: str
    data: ResultData



