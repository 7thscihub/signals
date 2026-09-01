import time
import traceback
import json
from mooneazy.scripts.analysis import get_signals
from mooneazy.alerts.sounds import play_alert
from mooneazy.scripts import util

ALERT_UPTIME = 90

def get_signals_or_error():
    signals = None
    error = None
    try:
        signals = get_signals()
    except Exception as e:
        error = e
    return signals, error
    

def get_active_signals(signals:list[dict])->list[dict]:
    active_signals = []
    if not signals:
        return None
    for signal in signals:
        if not signal:
            continue
        signal['utc_time'] = util.unix_to_utc(signal['trigger_time'])
        if util.is_active_signal(signal["time"], signal["interval"]):
            active_signals.append(signal)
    return active_signals

def get_scalping_signals():
    signals, error = get_signals_or_error()
    active_signals = get_active_signals(signals)
    return active_signals, error

def print_active_signals(signals):
    active_signals = get_active_signals(signals)
    for signal in active_signals:
        print(json.dumps(signal, indent=4))
        

def play_alert():
    from alerts import sounds
    sounds.play_alert()


def scalper():
    while True:
        signals, error = get_signals_or_error()
        if error:
            print('erro eroor eorro')
            play_alert()
            time.sleep(60)
            continue
        if signals:
            if active_signals:= get_active_signals(signals):
                print('signaaaaaaaaaaaalsssss')
                print_active_signals(active_signals)
                play_alert()
        time.sleep(300)

def scalper_debugger():
    signals = get_signals()
    simple_views = []
    for signal in signals:
        simple_signal = {
            "symbol": signal['symbol'],
            "trigger_time": util.unix_to_utc(signal['trigger_candle']['time']),
            "entry_price": signal['trigger_candle']['close'],
            "signal_type": signal['signal_type'],
            "inerval": signal['interval']
        }
        simple_views.append(simple_signal)
    print(json.dumps(simple_views, indent=4))


if __name__ == "__main__":
    print("Scalper running...")
    scalper_debugger()
