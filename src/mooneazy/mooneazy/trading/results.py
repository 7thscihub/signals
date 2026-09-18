from typing import Literal, TypedDict
from pydantic import BaseModel, validate_call, RootModel
import ..candles_api.api as candles_api
from . import util


class Candle(TypedDict):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: float


class SignalModel(TypedDict):
    symbol: str
    interval: str
    time: int
    signal_type: str
    entry_price: float
    sl: float
    tps: tuple 


class Result(TypedDict):
    target: float
    status: Literal['pending', 'success', 'failed']


@validate_call(validate_return=True)
def get_candles(symbol: str, interval: str, start_time: str) -> list[Candle]:
    parameters = {
        'interval': interval, 'start_time': start_time, 'symbol': symbol
    }
    return candles_api.get_candles(parameters)


@validate_call(validate_return=True)
def get_signal_results(signal:SignalModel) -> dict[int, Result]:
    candles = get_candles(
        symbol=signal['symbol'],
        interval=signal['interval'],
        start_time=signal['time']
    )
    return util.get_results(candles=candles, signal=signal)


@validate_call(validate_return=True)
def get_results(signals:list[SignalModel]):
    results = []
    for siganal in signals:
        results.append(get_signal_results(signal))
    return results




