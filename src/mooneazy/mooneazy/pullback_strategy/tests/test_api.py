from candles_api.candles_api.api import get_candles
import pytest
from pullback_strategy.tests import api_test_data 


def test_missing_symbol():
    parameters = {
        'limit': 20, 'interval': '4h',
    }
    supported_symbols = api_test_data.SUPPORTED_SYMBOLS
    with pytest.raises(KeyError):
        get_candles(parameters=parameters, supported_symbols=supported_symbols)



