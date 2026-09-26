import copy
import time
from typing import Literal
from pydantic import BaseModel, validate_call
from ..candles_api.candles_api import api
from . import tps
from . import models


@validate_call()
def get_signal_candles(
        symbol: str, interval: str, 
        start_time: int, limit:int = 1500
    ) -> list[dict]:
    parameters = {
        'interval': interval, 
        'start_time': start_time, 
        'symbol': symbol,
        'limit': limit
    }
    return api.get_candles(parameters)


@validate_call()
def get_signal_results(signal:models.SignalModel) -> dict | None:
    signal_dict = signal.model_dump()
    signal_data = signal_dict['data']
    candles = get_signal_candles(
        symbol=signal_data['symbol'],
        interval=signal_data['interval'],
        start_time=signal_data['time'],
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
            results.append(signal_results)
    return results





