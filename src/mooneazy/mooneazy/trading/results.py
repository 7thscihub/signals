from typing import Literal
from pydantic import BaseModel, validate_call, RootModel
from ..candles_api.candles_api import api
from . import util


class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: float


class SignalData(BaseModel):
    symbol: str
    interval: str
    time: int
    signal_type: str
    entry_price: float
    sl: float
    tps: tuple 


class SignalModel(BaseModel):
    id: str
    data: SignalData


class Result(BaseModel):
    target: float
    status: Literal['pending', 'success', 'failed']


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
def get_signal_results(signal_data:SignalData) -> dict[int, dict]:
    candles = get_candles(
        symbol=signal_data.symbol,
        interval=signal_data.interval,
        start_time=signal_data.time
    )
    return util.get_results(candles=candles, signal=signal)


@validate_call()
def get_results(signals:list[SignalModel]):
    results = []
    for siganal in signals:
        results.append(get_signal_results(signal.data))
    return results




