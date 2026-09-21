import copy
from typing import Literal
from pydantic import BaseModel, validate_call, RootModel
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
    id: str
    data: SignalData


@validate_call()
def get_candles(symbol: str, interval: str, start_time: str) -> list[dict]:
    candles = []
    parameters = {
        'interval': interval, 'start_time': start_time, 'symbol': symbol
    }
    candles = api.get_candles(parameters)
    for candle in candles:
        candles.append(Candle.model_validate(candle).model_dump())
    return candles


@validate_call()
def get_updated_signal(signal:SignalModel) -> dict | None:
    signal_data[dict] = signal.data.model_dump()
    candles = get_candles(
        symbol=signal_data.symbol,
        interval=signal_data.interval,
        start_time=signal_data.time
    )
    updated_signal_data = tps.get_results(
        candles=candles,
        signal_data=signal_data
    )
    if updated_signal_data != original_signal_dict:
        signal.data = updated_signal_data
        return signal.model_dump()
    return None

def build_signal_model():


@validate_call()
def get_updated_signals(signals:list[dict]) -> list[dict]:
    updated_signals = []
    for signal in signals:

        if upddated_signal:= get_updated_signal(signal):
            upddated_signals.append(signal)
    
    return updated_signals or none






