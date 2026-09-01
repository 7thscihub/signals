from mooneazy.pullback_strategy.pullback_strategy import pivots
from mooneazy.pullback_strategy.pullback_strategy import fakeouts
from mooneazy.pullback_strategy.pullback_strategy import trading


def is_btw(test_candle, left_candle, right_candle):
    test_time = int(test_candle['time'])
    left_time = int(left_candle['time'])
    right_time = int(right_candle['time'])
    return left_time < test_time < right_time


def get_candles_between(candles, start_candle, end_candle):
    start_time = int(start_candle['time'])
    end_time = int(end_candle['time'])
    return [c for c in candles if start_time < int(c['time']) < end_time]


def get_hs_buy_level(candles, lookback):
    left_shoulder = {}
    neck_line = {}
    lower_lows = pivots.get_lower_lows(candles, lookback)
    if len(lower_lows) < 2:
        return None, None
    
    left_shoulder_candle = lower_lows[-2]
    head_candle = lower_lows[-1]
    left_shoulder = {
        'time': int(left_shoulder_candle['time']),
        'low': float(left_shoulder_candle['low'])
    }
    neck_line_candles = get_candles_between(candles, left_shoulder_candle, head_candle)
    neck_line = max(c['high'] for c in neck_line_candles)
    right_shoulder_candles = get_candles_between(candles, head_candle, candles[-1])
    first_hh = max(c['high'] for c in right_shoulder_candles) > neck_line

    if first_hh:
        return left_shoulder, head_candle
    return None, None
 
 
def get_hs_sell_level(candles, lookback)->tuple[dict] | None:
    left_shoulder = {}
    neck_line = {}
    higher_highs = pivots.get_higher_highs(candles, lookback)
    if not higher_highs or len(higher_highs) < 2:
        return None, None
    
    left_shoulder_candle = higher_highs[-2]
    head_candle = higher_highs[-1]
    left_shoulder = {
        'time': int(left_shoulder_candle['time']),
        'high': float(left_shoulder_candle['high'])

    }
    neck_line_candles = get_candles_between(candles, left_shoulder_candle, head_candle)
    neck_line = min(c['low'] for c in neck_line_candles)
    right_shoulder_candles = get_candles_between(candles, head_candle, candles[-1])
    first_ll = min(c['low'] for c in right_shoulder_candles) < neck_line
    
    if first_ll:
        return left_shoulder, head_candle
    return None, None


def get_trade_signals(signals, tp_rrs:tuple=(2, 5), sl_padding:int=0.001):
    if not signals:
        return None
    trade_signals = []
    tp1_rrr = min(tp_rrs)
    tp2_rrr = max(tp_rrs)
    for signal in signals:
        trade_signals.append(make_trade_signal(
            signal=signal, 
            tp1_rrr=tp1_rrr,
            tp2_rrr=tp2_rrr,
            sl_padding=sl_padding
        ))
    return trade_signals


def make_trade_signal(signal, tp_rrrs, sl_padding) -> dict:
    signal_type = (
        'h&s_pullback_' + signal['signal_type']
    )
    signal['signal_type'] = signal_type
    trade_signal = trading.get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal


def get_latest_signals(
        candles, 
        pivot_lookback, 
        fo_lookback=3,
    )->list[dict]:
    buy_shoulder, buy_head = get_hs_buy_level(candles, lookback=pivot_lookback)
    sell_shoulder, sell_head = get_hs_sell_level(candles, lookback=pivot_lookback)
    buy_levels, sell_levels = None, None
    if buy_shoulder:
        buy_levels = [{'time': buy_head['time'], 'value': buy_shoulder['low']}]
    if sell_shoulder:   
        sell_levels = [{'time': sell_head['time'], 'value': sell_shoulder['high']}]
    signals = fakeouts.get_all_signals(
        candles, 
        buy_levels=buy_levels, 
        sell_levels=sell_levels, 
        fo_lookback=fo_lookback
    )
    return signals

def is_on_sr(candles, lookback, signal, fib=0.8):
    range_low = pivots.get_range_low(candles, lookback)['low']
    range_high = pivots.get_range_high(candles, lookback)['high']
    
    support_fib_price = range_high - (range_high - range_low) * fib 
    resistance_fib_price = range_low + (range_high - range_low) * fib 
    signal_direction = 'buy' if 'buy' in signal['signal_type'] else 'sell'
    if signal_direction == 'buy':
        return int(signal['lookback_hl']) <= int(support_fib_price)
    return signal['lookback_hl'] >= resistance_fib_price


class HeadAndShoulder:
    def __init__(self, candles, configs):
        if len(candles) < 200:
            raise ValueError(
                f"""heads and shoulder signals require 200 candles to work properly."""
            )
        self._candles = candles[-205:]
        self._configs = configs
        self._pivot_lookback = configs.hs_pivot_lookback 
        self._fo_lookback = configs.hs_fo_lookback
        self._tp_rrrs = configs.hs_tp_rrrs
        self._sl_padding = configs.sl_padding
        self._sr_fib = configs.sr_fib
    

    def buy_levels(self):
        return get_hs_buy_level(self._candles, self._pivot_lookback)

    def sell_levels(self):
        return get_hs_sell_level(self._candles, self._pivot_lookback)
    
    def latest_signals(self):
        return get_latest_signals(self._candles, self._pivot_lookback, self._fo_lookback)

    def latest_trade_signal(self):
        signals = self.latest_signals()
        sr_signals = [signal for signal in signals if is_on_sr(
            candles=self._candles, lookback=self._pivot_lookback, signal=signal, fib=self._sr_fib
        )]
        trade_signals = get_trade_signals(
            sr_signals, tp_rrs=self._tp_rrrs, sl_padding=self._sl_padding
        )
        latest_signal = trade_signals[0] if trade_signals else None
        return latest_signal
