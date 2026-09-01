
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

