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
def get_signal_results(signal:[SignalModel]) -> SignalModel:
    signal_data = signal.data 
    candles = get_candles(
        symbol=signal_data.symbol,
        interval=signal_data.interval,
        start_time=signal_data.time
    )
    signal_results = tps.get_results(candles=candles, signal_data=signal_data)
    for i in range(len(signal_results)):
        tp_key = f'tp{i + 1}'
        setattr(signal_data, tp_key, i)
    return signal


@validate_call()
def get_results(signals:list):
    results = []
    for siganal in signals:
        results.append(get_signal_results(signal))
    return results




