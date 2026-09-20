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
    tp1: Tp
    tp2: Tp 


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


@validate_call(validate_return=True)
def get_updated_signal(signal:SignalModel) -> SignalModel:
    signal_copy = copy.deepcopy(signal)
    signal_data[dict] = signal_copy.data.model_dump()
    candles = get_candles(
        symbol=signal_data.symbol,
        interval=signal_data.interval,
        start_time=signal_data.time
    )
    signal_tps[dict] = tps.collect_tps(signal_data)
    signal_results[dict] = tps.get_results(
        candles=candles, 
        signal_data=signal_data
    )
    for k, v in signal_results.items():
        if k not in signal_data.keys() or v != signal_tps[k]:
            setattr(signal_copy, k, v) 
    updated_signal_dict = signal_copy.model_dump()
    original_signal_dict = signal.model_dump()
    if signal_copy_dict == original_signal_dict:
        return signal_copy_dict
    return None


@validate_call()
def get_updated_signals(signals:list[SignalModel]):
    updated_signals = []
    for signal in signals:
        updated_signal = get_updated_signal(signal)
        if not upddated_signal:
            continue
        updated_signals.append(updated_signal)
    return updated_signals




