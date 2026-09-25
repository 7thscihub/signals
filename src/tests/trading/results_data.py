SIGNAL_DATA = {
    'symbol': 'BTCUSDT',
    'interval': '30m',
    'time': 1788768000000,
    'signal_type': 'sfp_buy',
    'entry_price': 79429.9,
    'sl': 78859.7613,
    'tp1': 80285.10805,
    'tp2': 81140.3161,
    'tp1_status': 'pending',
    'tp2_status': 'pending',
    'status': 'pending',
}


UPDATED_SIGNAL_DATA = {
    **SIGNAL_DATA,
    'tp1_status': 'success',
    'status': 'partial',
}


CANDLES = [
    {
        'time': 1788768060000,
        'open': 79429.9,
        'high': 80300.0,
        'low': 79300.0,
        'close': 80200.0,
    },
]


SIGNAL_DICT = {
    "$id": 'signals_0003',
    'data': SIGNAL_DATA,
}


UPDATED_SIGNAL_DICT = {
    "id": 'signals_0003',
    'data': UPDATED_SIGNAL_DATA,
}


SIGNALS = [
    {   "$id": 'signals_0003',
        'data': SIGNAL_DATA,
    },
    {   '$id': 'signals_0004',
        'data': {
            **SIGNAL_DATA,
            'time': 1788768100000,
        },
    },
]


UPDATED_RESULTS = [
    {   "$id": 'signals_0003',
        'data': UPDATED_SIGNAL_DATA,
    },
]
