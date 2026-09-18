from pydantic import BaseModel

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


class SignalModel(BaseModel):
    $id: str
    data: SignalData


class ResultData(BaseModel):
    tp1_results: Literal['sucess', 'pending', 'failed']
    tp2_results: Literal['sucess', 'pending', 'failed']


class ResultModel(BaseModel):
    $id: str
    data: ResultData


def flatten_rows(rows: list[dict]) -> list[]:
    flat_rows = []
    for row in rows:
        row['$id'] = 



