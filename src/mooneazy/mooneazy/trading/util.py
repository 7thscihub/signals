
def touches(candle, value):
    return float(candle['high']) >= float(value) >= float(candle['low'])


def get_results_candles(signal):
    parameters = {
        'symbol': signal['symbol'],
        'interval': signal['interval'],
        'start_time': signal['start_time']
    }

def update_failed_tps(tps_dict):
    for k, v in tps_dict.items():
        # skip targets that have already been hit 
        if v['status'] == 'success':
            continue
        v['status'] = 'failed'


def update_successful_tps(tps_dict):
    for k, v in tps_dict.items():
        if touches(candle, v['target']):
            v['status'] = 'success'


def get_results(candles, signal):
    tps = signal['tps']
    tps_dict = {}
    sorted_tps = sorted(tps)

    # create the default tps_dict
    for i in range(sorted_tps):
        tp = i + 1
        tps_dict[tp] = {'target': sorted_tps[i], 'status': 'pending'}
    
    for candle in candles:
        if int(candles['time']) <= int(signal['time']):
            continue
        if touches(candle, signal['sl']):
            update_failed_tps(tps_dict)
            break
        update_successful_tps(tps_dict)
    return tps_dict




