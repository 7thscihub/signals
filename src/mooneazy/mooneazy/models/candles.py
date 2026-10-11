from typing import Literal
from pydantic import BaseModel, Field

class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    end_time: float 


