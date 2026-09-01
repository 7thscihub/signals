from mooneazy.scripts.scalper import get_scalping_signals
import json

if __name__ == '__main__':
    print("scalper_debugger running")
    signals, errors = get_scalping_signals()
    if errors:
        print(errors)
    if signals:
        print(json.dumps(signals, indent=4))
