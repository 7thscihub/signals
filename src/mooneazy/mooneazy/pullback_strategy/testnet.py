from ..candles_api.candles_api import api
from .pullback_strategy.pullback import get_valid_pullback_level
from ..scripts.util import unix_to_utc

def get_candles(symbol='BTCUSDT', interval='1d', limit=100):
    parameters = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit 
    }
    return api.get_candles(parameters)


pullback_level = get_valid_pullback_level(
    candles=get_candles(),
    lookback_left = 5,
    lookback_right = 10,
    trend = 'buy',
    min_fib = 0.236,
    max_fib = 0.65,
    min_follow_up_retracement_fib = 0.7
)


if __name__ == '__main__':
    print(pullback_level)

