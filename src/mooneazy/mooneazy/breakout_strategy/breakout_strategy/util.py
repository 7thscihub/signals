from mooneazy.breakout_strategy.breakout_strategy.trading import get_trade


def resolve_level(level):
    """
    extracts level values for levels passed as dicts
    and return a list of int
    """
    if isinstance(level, dict):
        level = level["value"]
    return level


def get_lookback_slice(
        candles:list, 
        candle_index:int, 
        fo_lookback:int
    ) -> list:
    if candle_index < fo_lookback:
        raise ValueError(
            f"""
            candle index value: {candle_index} is less than 
            lookback value {fo_lookback}
            """
        )
    
    start_index = candle_index - fo_lookback
    end_index = candle_index + 1
    len_candles = len(candles)
    if end_index > len_candles:
        raise ValueError(
            f"""
            len_candles: {len_candles} is less than candle_index: {candle_index}
            """
        )
    return candles[start_index:end_index]


def is_bullish(candle):
    return float(candle['close']) > float(candle['open'])


def get_lookback_slices(
        candle_index:int | None = None, 
        lookback:int | None = None, 
        **args
    ) -> dict[str:list]:
    if candle_index is None:
        raise ValueError(f"Provide Candle Index for lookback slicing")
    if lookback is None:
        raise ValueError(f"Provide Lookback Value for Lookback slicing")
    slices = {}
    for key, arg in args.items():
        slices[key] = get_lookback_slice(candles=arg, candle_index=candle_index, fo_lookback=lookback)
    return slices

def make_trade_signal(breakout_candle, interval, tp_rrrs, sl_padding, score):
    lookback_hl = breakout_candle['high']
    signal_type = 'engulfing_breakout_sell'
    if is_bullish(breakout_candle):
        lookback_hl = breakout_candle['low']
        signal_type = 'engulfing_breakout_buy'
    signal = {
        'trigger_candle': breakout_candle,
        'lookback_hl': lookback_hl,
        'signal_type': signal_type,
        'interval': interval,
        'score': score
    }
    trade_signal = get_trade(
        signal=signal, 
        tp1_rrr=tp_rrrs[0], 
        tp2_rrr=tp_rrrs[1], 
        sl_padding=sl_padding
    )
    return trade_signal
