from pydantic import BaseModel, validate_call
from typing import Collable, Literal 


class LevelModel(BaseModel):
    symbol: str 
    interval: str 
    time: str 
    value: float  
    level_type: str
    direction: Literal['buy', 'sell']


def valide_level(level):
    return LevelsModel.model_validate(level).model_dump()


class Level:
    @validate_call
    def __init__(self, symbol:str, interval:str, providers:dict[str, Collable]):
        self.symbol = symbol
        self.interval = interval
        self.providers = providers


def get_provider_levels(symbol, interval, provider, config):
    levels_list = []
    levels = provider(config[k])
    for level in levels:
        
    


