import copy
from typing import Literal
from pydantic import BaseModel, validate_call, Field
from ..candles_api.candles_api import api
from . import tps


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
    status: Literal['pending', 'success', 'failed']


class SignalModel(BaseModel):
    id: str = Field(alias='$id')
    data: SignalData


@validate_call()
def get_signal_candles(symbol: str, interval: str, start_time: int, limit:int) -> list[dict]:
    parameters = {
        'interval': interval, 'start_time': start_time, 'symbol': symbol
    }
    return api.get_candles(parameters)


@validate_call()
def get_signal_results(signal:SignalModel) -> dict | None:
    signal_dict = signal.model_dump()
    signal_data = signal_dict['data']
    candles = get_signal_candles(
        symbol=signal_data['symbol'],
        interval=signal_data['interval'],
        start_time=signal_data['time'],
        limit=500
    )
    updated_signal_data = tps.get_results(
        candles=candles,
        signal_data=signal_data
    )
    if updated_signal_data != signal_data:
        signal_dict['data'] = updated_signal_data
        return signal_dict
    return None


@validate_call()
def get_new_results(signals:list[dict]) -> list[dict]:
    results = []
    for signal in signals:
        if signal_results:= get_signal_results(signal):
            new_results.append(signal_results)
    return results





