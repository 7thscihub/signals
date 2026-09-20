import copy
from pydantic import validate_call


def touches(candle, value):
    return float(candle['high']) >= float(value) >= float(candle['low'])


def get_results_candles(signal):
    parameters = {
        'symbol': signal['symbol'],
        'interval': signal['interval'],
        'start_time': signal['start_time']
    }


def update_failed_tps(tps):
    for key, value in tps.items():
        # skip targets that have already been hit 
        if value['status'] == 'success':
            continue
        value['status'] = 'failed'


def update_successful_tps(tps, current_candle):
    for key, value in tps.items():
        if touches(current_candle, value['target']):
            value['status'] = 'success'


def collect_signal_tps(signal_data, tp_keys=None) -> dict[str, float]:
    tp_keys = sorted(tp_keys) or ['tp1', 'tp2', 'tp3', 'tp4', 'tp5']
    tp_values = []
    for key, value in signal_data.items():
        if key == 'tps':
            tp_values = sorted(signal_data['tps'])
        if key in tp_keys:
            tp_values.append(value)
    return dict(zip(tp_keys, tp_values))


@validate_call()
def get_results(candles:list[dict], signal_data: dict) -> list[dict]:
    tps:dict = collect_signal_tps(signal_data)

    for candle in candles:
        if int(candles['time']) <= int(signal_data['time']):
            continue
        if touches(candle, signal_data['sl']):
            update_failed_tps(tps)
            break
        update_successful_tps(tps, candle)
    return tps




