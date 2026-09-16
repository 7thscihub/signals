from typing import Literal, TypedDict
from pydantic import BaseModel, validate_call, RootModel
from ..candles_api import get_candles
from . import util

class SignalModel(TypedDict):
    symbol: str
    interval: str
    time: int
    signal_type: str
    entry_price: float
    sl: float
    tps: tuple 


class Candle(TypedDict):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: float


class Result(TypedDict):
    target: float
    status: Literal['pending', 'success', 'failed']



@validate_call(validate_return=True)
def get_results(signal:SignalModel) -> dict[int, Result]:
    candles:list[Candle] = get_candles(
        symbol=signal['symbol'],
        interval=signal['interval'],
        start_time=signal['time']
    )
    return util.get_results(candles=candles, signal=signal)





