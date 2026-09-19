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
    for tp in tps:
        # skip targets that have already been hit 
        if tp['status'] == 'success':
            continue
        tp['status'] = 'failed'


def update_successful_tps(tps, current_candle):
    for tp in tps_list:
        if touches(current_candle, tp['target']):
            tp['status'] = 'success'


def collect_signal_tps(signal_data, tp_keys=None):
    tps = []
    tp_keys = tp_keys or ['tp1', 'tp2', 'tp3', 'tp4', 'tp5']
    for key, value in signal_data.items():
        if key == 'tps':
            return value 
        if key in tp_keys:
            tps.append(value)
    return tps


@validate_call()
def get_results(candles:list[dict], signal_data: dict) -> list[dict]:
    tps:list = collect_signal_tps(signal_data)

    for candle in candles:
        if int(candles['time']) <= int(signal_data['time']):
            continue
        if touches(candle, signal_data['sl']):
            update_failed_tps(tps)
            break
        update_successful_tps(tps, candle)
    return tps




