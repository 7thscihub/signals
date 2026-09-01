from . import util


def get_bullish_fa(candles, level, fo_lookback):
    triggers = []
    for i, candle in enumerate(candles):
        lb_low = get_lb_low(candles, candle, level, i)
        if lb_low == "break":
            break
        if not lb_low:
            continue
        if fa := is_bullish_fa(candles, lb_low, level, fo_lookback, i):
            triggers.append(fa)
    return util.eliminate_triggers(triggers) if triggers else None


def get_bearish_fa(candles, level, fo_lookback):
    triggers = []
    for i, candle in enumerate(candles):
        lb_high = get_lb_high(candles, candle, level, i)
        if lb_high == "break":
            break
        if not lb_high:
            continue
        if fa := is_bearish_fa(candles, lb_high, level, fo_lookback, i):
            triggers.append(fa)

    return util.eliminate_triggers(triggers) if triggers else None


def get_bearish_sfp(candles, level, fo_lookback):
    triggers = []
    for i, candle in enumerate(candles):
        lb_high = get_lb_high(candles, candle, level, i)
        if lb_high == "break":
            break
        if not lb_high:
            continue
        if sfp := is_bearish_sfp(candles, lb_high, level, fo_lookback, i):
            triggers.append(sfp)

    return util.eliminate_triggers(triggers) if triggers else None


def get_bullish_sfp(candles, level, fo_lookback):
    triggers = []
    for i, candle in enumerate(candles):
        lb_low = get_lb_low(candles, candle, level, i)
        if lb_low == "break":
            break
        if not lb_low:
            continue
        if sfp := is_bullish_sfp(candles, lb_low, level, fo_lookback, i):
            triggers.append(sfp)
    return util.eliminate_triggers(triggers) if triggers else None


def get_bullish_fakeouts(candles, level, fo_lookback):
    triggers = []
    if sfp := get_bullish_sfp(candles, level, fo_lookback):
        triggers.extend(sfp)

    if fa := get_bullish_fa(candles, level, fo_lookback):
        triggers.extend(fa)

    return util.eliminate_triggers(triggers) if triggers else None


def get_bearish_fakeouts(candles, level, fo_lookback):
    triggers = []
    if sfp := get_bearish_sfp(candles, level, fo_lookback):
        triggers.extend(sfp)

    if fa := get_bearish_fa(candles, level, fo_lookback):
        triggers.extend(fa)

    return util.eliminate_triggers(triggers) if triggers else None


def get_all_sell_signals(candles, levels, fo_lookback):
    fos = []
    for level in levels:
        if fo := get_bearish_fakeouts(candles, level, fo_lookback):
            fos.extend(fo)
    return fos


def get_all_buy_signals(candles, levels, fo_lookback):
    fos = []
    for level in levels:
        if fo := get_bullish_fakeouts(candles, level, fo_lookback):
            fos.extend(fo)
    return fos


def get_lb_high(candles, candle, level, candle_index):
    """
    returns the highest high since the level was formed
    """
    if not level:
        return None
    if int(candle["time"]) <= int(level["time"]):
        return None
    prev_candles = candles[:candle_index + 1]
    if util.is_tested(prev_candles, level, "sell"):
        return "break"
    lb_candles = get_level_candles(candles, level, candle_index)
    if not lb_candles:
        return None

    return max(c["high"] for c in lb_candles)


def get_lb_low(candles, candle, level, candle_index):
    """
    returns the lowest low since the level was form
    """
    if not level:
        return None
    if int(candle["time"]) <= int((level["time"])):
        return None
    prev_candles = candles[:candle_index + 1]
    if util.is_tested(prev_candles, level, "buy"):
        return "break"
    lb_candles = get_level_candles(candles, level, candle_index)
    if not lb_candles:
        return None

    return min(c["low"] for c in lb_candles)


def get_level_candles(candles, level, candle_index):
    for i, candle in enumerate(candles):
        if candle["time"] == level["time"]:
            return candles[i:candle_index + 1]
    return None


def get_fo_range_details(candles, fo_lookback, candle_index):
    """
    fo_range is the minimum number of lookback candles
    reviewed to check for a single fakeout trigger
    """
    fo_candles = util.get_lookback_candles(candles, fo_lookback, candle_index)
    return util.get_range_details(fo_candles)


def is_bearish_sfp(candles, lb_high, level, fo_lookback, candle_index):
    min_oc, min_low, max_oc, max_high = get_fo_range_details(
        candles, fo_lookback, candle_index)

    if max_high != lb_high:
        return False
    level_value = util.resolve_level(level)
    candle = candles[candle_index]
    if candle["close"] < candle["open"] <= max_oc <= level_value < max_high:
        return {
            "trigger_candle": candle, "lookback_hl": max_high, "signal_type": "sfp_sell", "level": level_value
        }
    return False


def is_bullish_sfp(candles, lb_low, level, fo_lookback, candle_index):
    min_oc, min_low, _, _ = get_fo_range_details(candles, fo_lookback, candle_index)
    if min_low != lb_low:
        return False
    level_value = util.resolve_level(level)
    candle = candles[candle_index]
    if candle["close"] > candle["open"] >= min_oc >= level_value > min_low:
        return {
            "trigger_candle": candle, "lookback_hl": min_low, "signal_type": "sfp_buy", "level": level_value
        }
    return False


def is_bullish_fa(candles, lb_low, level, fo_lookback, candle_index):
    min_oc, min_low, max_oc, max_high = get_fo_range_details(
        candles, fo_lookback, candle_index
    )
    if min_low != lb_low:
        return False
    level_value = util.resolve_level(level)
    candle = candles[candle_index]
    if min_oc < level_value < max_oc and candle["close"] > level_value > candle["low"]:
        return {"trigger_candle": candle, "lookback_hl": min_low, "signal_type": "fa_buy", "level": level_value}
    return False


def is_bearish_fa(candles, lb_high, level, fo_lookback, candle_index):
    min_oc, min_low, max_oc, max_high = get_fo_range_details(
        candles, fo_lookback, candle_index
    )
    if max_high != lb_high:
        return False
    level_value = util.resolve_level(level)
    candle = candles[candle_index]
    if max_oc > level_value > min_oc and candle["close"] < level_value < candle["high"]:
        return {
            "trigger_candle": candle, 
            "lookback_hl": max_high, 
            "signal_type": "fa_sell", 
            "level": level_value
            }
    return False

def get_all_signals(
        candles:list[dict], 
        buy_levels:list[dict] | None = None, 
        sell_levels:list[dict] | None=None, 
        fo_lookback:int=5
    )->list[dict]:
    """
    Returns a list of dicts with keys trigger_candle, 
    lookback_hl, signal_type and level
    """
    all_signals = []
    if buy_levels:
        buy_signals = get_all_buy_signals(candles,  buy_levels, fo_lookback)
        all_signals.extend(buy_signals)
    if sell_levels:
        sell_signals = get_all_sell_signals(candles,  sell_levels, fo_lookback)
        all_signals.extend(sell_signals)        
    return all_signals


def get_active_signals(candles, interval, buy_levels=[], sell_levels=[], fo_lookback=5):
    # print(f'buy_levels: {buy_levels}, sell levels: {sell_levels}')
    active_signals = []
    signals = get_all_signals(candles, buy_levels, sell_levels, fo_lookback)
    print(f'signals: {signals}')
    for signal in signals:
        signal_time = signal['trigger_candle']["time"]
        if util.is_active_signal(signal_time, interval):
            active_signals.append(signal)
    return active_signals

