import json
from . import binance
from . import yahoo
from . import config


def get_candles(parameters: dict = None, supported_symbols: dict[set] = None)->list[dict]:
    '''fetching candle stick data from either binance  or yahoo apis
    
    Args:
        Parameters: A dictionary of api params:
            symbol: Ticker string (e.g., 'AAPL', 'BTCUSD').
            limit: Exact number of latest candles to return.
            interval: Time interval per candle (e.g., '1d', '1h', '15m', '1m').
            start_time: The ealierst candle time in unix UTC time
            end_time: The latest candles time
            Start time is required if the limit is not indicated
        Supported_symbols: Dictionary of a list/sets of supported symbols 
            with keys crypto commodies and forex
    Returns:
        A list of dictionaries containing individual candle data.
    '''
    supported_symbols = supported_symbols or config.SUPPORTED_SYMBOLS
    api_server = None
    try:
        if parameters['symbol'] in supported_symbols['binance']:
            api_server = binance
        else:
            api_server = yahoo
    except KeyError:
        raise KeyError(
            'provide symbol in parameters dict '
            'and provide a dict of dict with key crypto with supported crypto symbol'
        )

    return api_server.get_candles(parameters=parameters)


def download_candles(parameters, file_path, supported_symbols=None):
    candles = get_candles(parameters, supported_symbols)
    with open(file_path, 'w') as f:
        json.dump(candles, f, indent=4)


def get_candles_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
    
