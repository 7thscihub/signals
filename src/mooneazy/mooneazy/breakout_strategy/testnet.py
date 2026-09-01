import json
from breakout_strategy import emas, hma
from breakout_strategy.breakout import count_indicator_touches
from tests.test_data import breakout_data

def main():
    test_data = breakout_data.score_5_data
    candles = test_data['breakout_candles']
    hull_values = test_data['hull_55_values']

    touches = count_indicator_touches(candles, hull_values)
    # print(touches)

if __name__ == '__main__':
    main()
    