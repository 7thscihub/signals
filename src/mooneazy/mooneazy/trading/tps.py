import copy
from pydantic import validate_call


TP_KEYS = ['tp1', 'tp2', 'tp3', 'tp4', 'tp5']
TP_STATUS_KEYS = [
    'tp1_status', 'tp2_status', 'tp3_status', 'tp4_status', 'tp5_status'
]


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


def collect_signal_tps(
    signal_data: dict, tp_keys:list=TP_KEYS, tp_status_keys: list=TP_STATUS_KEYS
    ) -> dict[str, dict]:
    tp_keys = sorted(tp_keys)
    tp_status_keys = sorted(tp_status_keys)
    tps_dict= {}
    for i in range(len(tp_keys)):
        tp_key:str = tp_keys[i]
        target = signal_data.get(tp_key, None)
        if not target:
            continue
        tp_details = {
            'target': target,
            'status': signal_data[tp_status_keys[i]]
        }
        tps_dict[tp_key] = tp_details

    return tps_dict


def get_results(candles:list[dict], signal_data: dict) -> dict[str, dict]:
    """
    returns an update signal_data dictionary with updated status for the
    """

    tps:dict = collect_signal_tps(signal_data)
    results = copy.deepcopy(signal_data)
    stop_loss = signal_data['sl']
    for candle in candles:
        if int(candle['time']) <= int(signal_data['time']):
            continue
        if touches(candle, stop_loss):
            update_failed_tps(tps)
            results['status'] = 'failed'
            break
        update_successful_tps(tps, candle)

    for key, value in tps.items():
        results[f"{key}_status"] = value['status'] 

    return results




