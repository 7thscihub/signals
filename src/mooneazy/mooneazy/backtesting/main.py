from backtesting.breakouts import Breakouts
from breakout_strategy.breakout_strategy import breakout
from candles_api.candles_api import api
from backtesting.breakout_util import get_lookback_slice
from breakout_strategy.breakout_strategy import breakouts
import datetime
import json


def unix_to_utc(unix_timestamp):
    return datetime.datetime.fromtimestamp(unix_timestamp / 1000, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def get_candles():
    parameters = {'symbol': 'BTCUSDT', 'interval': '30m', 'limit': 200}
    candles = api.get_candles(parameters=parameters)
    return candles

def main():
    candles = get_candles()
    breakouts = Breakouts(
        trading_tf_candles=candles,
        fo_lookback=5,
        fast_ema_period=8,
        slow_ema_period=20,
        hull_period=55,
        min_opposite_candles=2
    )
    valid_breakouts = breakouts.get_trade_signals()
    for breakout in valid_breakouts:
        print(json.dumps(breakout, indent=4))
        # print(unix_to_utc(breakout['time']))

def get_engulfing_breakouts(fo_lookback=5, min_opposite_candles=2):
    candles = get_candles()
    breakouts = []
    for i in range(fo_lookback, len(candles)):
        lookback_candles = get_lookback_slice(candles=candles, candle_index=i, fo_lookback=fo_lookback)
        if breakout.is_engulfing_breakout(
                lookback_candles=lookback_candles[:-1],
                breakout_candle=lookback_candles[-1],
                min_opposit=2
            ):
            breakouts.append(candles[i])
    if not breakouts:
        return None
    for b in breakouts:
        print(unix_to_utc(b['time']))


def test_breakout_ts_breakouts():
    candles = get_candles()
    brkouts = breakouts.Breakouts(
        trading_tf_candles=candles,
    )
    latest = brkouts.get_latest_trade_signal()
    # for breakout in valid_breakouts:
    print(unix_to_utc(latest['trigger_candle']['time']))
    # print(json.dumps(latest, indent=4))


if __name__ == "__main__":
    test_breakout_ts_breakouts()
