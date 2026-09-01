from candles_api.api import get_candles
import candles_api.config as config

def main():
    supported_symbols = config.SUPPORTED_SYMBOLS
    parameters = {
        'symbol': 'GLD', 'interval': '15m', 'limit': 100
    }
    print(get_candles(parameters=parameters, supported_symbols=supported_symbols))

if __name__ == "__main__":
    main()
