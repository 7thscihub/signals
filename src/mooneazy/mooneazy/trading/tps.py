import copy
from typing import Literal
from pydantic import BaseModel
from ..candles_api.candles_api import api


TP_KEYS = ['tp1', 'tp2', 'tp3', 'tp4', 'tp5']

TP_STATUS_KEYS = [
    'tp1_status',
    'tp2_status',
    'tp3_status',
    'tp4_status',
    'tp5_status'
]

LOWER_TIMEFRAME_INTERVAL = '1m'

def touches(candle, value):
    return float(candle['high']) >= float(value) >= float(candle['low'])


def get_signal_candles(
        symbol: str, interval: str, start_time: int, limit: int
    ) -> list[dict]:
    parameters = {
        'interval': interval,
        'start_time': start_time,
        'symbol': symbol,
        'limit': limit
    }

    return api.get_candles(parameters)


def collect_signal_tps(
        signal_data: dict, tp_keys=TP_KEYS, tp_status_keys=TP_STATUS_KEYS
    ) -> dict[str, dict]:

    tp_keys = sorted(tp_keys)
    tp_status_keys = sorted(tp_status_keys)
    tps_dict = {}

    for i in range(len(tp_keys)):
        tp_key: str = tp_keys[i]
        target = signal_data.get(tp_key)
        if target is None:
            continue
        tp_details = {
            'target': target,
            'status': signal_data.get(tp_status_keys[i])
        }
        tps_dict[tp_key] = tp_details

    return tps_dict


def get_interval_minutes(interval: str) -> int:
    value = int(interval[:-1])
    unit = interval[-1].lower()
    interval_multiplier = {'m': 1, 'h': 60, 'd': 24 * 60 }
    try:
        return value * interval_multiplier[unit]
    except KeyError:
        raise KeyError(f'Unsupported interval: {interval}')


def is_stopped_lower_timeframe(candles, stop_loss, tp):
    """
    Determine whether the stop loss or take profit was reached first
    using lower-timeframe candles.

    """
    for candle in candles:
        sl_touched = touches(candle, stop_loss['value'])
        tp_touched = touches(candle, tp['target'])

        if sl_touched and not tp_touched:
            return True

        if tp_touched and not sl_touched:
            return False

        if sl_touched and tp_touched:
            # Both were touched in the same lower-timeframe candle.
            # OHLC data cannot determine which was reached first.
            return False

    return False


def resolve_with_lower_time_frame(
        signal_data, stop_loss, tp,
        lower_timeframe_interval: str = LOWER_TIMEFRAME_INTERVAL
    ):
    start_time = stop_loss['time']
    limit = get_interval_minutes(signal_data['interval'])

    lower_timeframe_candles = get_signal_candles(
        symbol=signal_data['symbol'],
        interval=lower_timeframe_interval,
        start_time=start_time,
        limit=limit
    )

    result = is_stopped_lower_timeframe(
        lower_timeframe_candles,
        stop_loss,
        tp
    )

    return result


def is_stopped_out(
        stop_loss, tp, signal_data,
        lower_timeframe_interval: str = LOWER_TIMEFRAME_INTERVAL
    ):
    if stop_loss['time'] is None:
        return False

    if tp['time'] is None:
        return True

    if stop_loss['time'] != tp['time']:
        return stop_loss['time'] < tp['time']

    return resolve_with_lower_time_frame(
        signal_data,
        stop_loss,
        tp,
        lower_timeframe_interval
    )


def get_signal_status(tps):
    statuses = [tp['status'] for tp in tps.values()]

    if not statuses:
        return 'pending'

    successful = statuses.count('success')
    failed = statuses.count('failed')

    if successful == len(statuses):
        return 'success'

    if successful > 0:
        return 'partial'

    if failed > 0:
        return 'failed'

    return 'pending'


def get_results(candles, signal_data):
    tps = collect_signal_tps(signal_data)
    results = copy.deepcopy(signal_data)

    stop_loss = {
        'value': signal_data['sl'],
        'time': None
    }

    # Find the first candle that touches the stop loss.
    for candle in candles:
        if touches(candle, stop_loss['value']):
            stop_loss['time'] = candle['time']
            break

    for key, value in tps.items():
        value['time'] = None

        for candle in candles:
            if touches(candle, value['target']):
                value['time'] = candle['time']
                break

        if is_stopped_out(
                stop_loss=stop_loss,
                tp=value,
                signal_data=signal_data
            ):
            value['status'] = 'failed'

        elif value['time'] is not None:
            value['status'] = 'success'

        else:
            value['status'] = 'pending'

    for key, value in tps.items():
        results[f"{key}_status"] = value['status']

    results['status'] = get_signal_status(tps)

    return results

