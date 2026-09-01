import json
from pullback_strategy.setups import get_setup_signals

def main():
    signals = get_setup_signals()
    print(signals)

if __name__ == '__main__':
    main()
    


