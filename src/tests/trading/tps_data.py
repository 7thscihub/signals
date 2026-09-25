SIGNAL_DATA = {
    'symbol': 'BTCUSDT',
    'interval': '30m',
    'time': 1000,
    'signal_type': 'sfp_buy',
    'entry_price': 100.0,
    'sl': 95.0,
    'tp1': 105.0,
    'tp2': 110.0,
    'tp1_status': 'pending',
    'tp2_status': 'pending',
    'status': 'pending'
}


CANDLES_NO_HIT = [
    {
        'time': 1000,
        'open': 100,
        'high': 103,
        'low': 98,
        'close': 101
    },
    {
        'time': 1060,
        'open': 101,
        'high': 104,
        'low': 99,
        'close': 103
    }
]


CANDLES_TP1 = [
    {
        'time': 1000,
        'open': 100,
        'high': 106,
        'low': 99,
        'close': 104
    },
    {
        'time': 1060,
        'open': 104,
        'high': 107,
        'low': 103,
        'close': 105
    }
]


CANDLES_SL = [
    {
        'time': 1000,
        'open': 100,
        'high': 102,
        'low': 94,
        'close': 96
    }
]


CANDLES_TP1_THEN_TP2 = [
    {
        'time': 1000,
        'open': 100,
        'high': 106,
        'low': 99,
        'close': 105
    },
    {
        'time': 1060,
        'open': 105,
        'high': 111,
        'low': 104,
        'close': 110
    }
]


CANDLES_SL_THEN_TP1 = [
    {
        'time': 1000,
        'open': 100,
        'high': 101,
        'low': 94,
        'close': 95
    },
    {
        'time': 1060,
        'open': 95,
        'high': 106,
        'low': 94,
        'close': 105
    }
]


CANDLES_BOTH_TOUCHED = [
    {
        'time': 1000,
        'open': 100,
        'high': 106,
        'low': 94,
        'close': 100
    }
]


LOWER_TIMEFRAME_CANDLES_TP = [
    {
        'time': 1000,
        'open': 100,
        'high': 106,
        'low': 99,
        'close': 105
    }
]


LOWER_TIMEFRAME_CANDLES_SL = [
    {
        'time': 1000,
        'open': 100,
        'high': 101,
        'low': 94,
        'close': 95
    }
]


LOWER_TIMEFRAME_CANDLES_BOTH = [
    {
        'time': 1000,
        'open': 100,
        'high': 106,
        'low': 94,
        'close': 100
    }
]


TP_DATA = {
    'tp1': {
        'target': 105.0,
        'status': 'pending'
    },
    'tp2': {
        'target': 110.0,
        'status': 'pending'
    }
}


STOP_LOSS = {
    'value': 95.0,
    'time': 1000
}


TP_PENDING = {
    'target': 105.0,
    'time': None,
    'status': 'pending'
}


TP_SUCCESS = {
    'target': 105.0,
    'time': 1000,
    'status': 'success'
}


TP_FAILED = {
    'target': 105.0,
    'time': 1000,
    'status': 'failed'
}
