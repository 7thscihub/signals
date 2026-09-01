from mooneazy.tests.test_data.setup_data import SETUP_DATA
from mooneazy.ultimate_setups.strategies.ultimate_setups import UltimateSetups 


def test_sfp_buy():
    data = SETUP_DATA
    setup = UltimateSetups(
        candles=data['sfp_buy_candles'],
        buy_levels=data['buy_levels'],
        sell_levels=data['sell_levels'],
        pivot_lookback=data['pivot_lookback'],
        fo_lookback=data['fo_lookback']
    )

    signals = setup.get_signals()
    assert signals[-1]['trigger_candle'] == data['sfp_buy_candles'][-1]

    in_trend_signals = setup.get_in_trend_signals(
        htf1_trend=data['htf1_trend'], htf2_trend=data['htf2_trend']
    )
    assert in_trend_signals[-1]['trigger_candle'] == data['sfp_buy_candles'][-1]


def test_sfp_sell():
    data = SETUP_DATA
    setup = UltimateSetups(
        candles=data['sfp_sell_candles'],
        buy_levels=data['buy_levels'],
        sell_levels=data['sell_levels'],
        pivot_lookback=data['pivot_lookback'],
        fo_lookback=data['fo_lookback']
    )
    signals = setup.get_signals()
    assert signals[-1]['trigger_candle'] == data['sfp_sell_candles'][-1]
    
    in_trend_signals = setup.get_in_trend_signals(
        htf1_trend=data['htf1_trend'], htf2_trend=data['htf2_trend']
    )
    assert in_trend_signals[-1]['trigger_candle'] == data['sfp_sell_candles'][-1]

    

def test_fa_buy():
    data = SETUP_DATA
    setup = UltimateSetups(
        candles=data['fa_buy_candles'],
        buy_levels=data['buy_levels'],
        sell_levels=data['sell_levels'],
        pivot_lookback=data['pivot_lookback'],
        fo_lookback=data['fo_lookback']
    )
    signals = setup.get_signals()
    assert signals[-1]['trigger_candle'] == data['fa_buy_candles'][-1]

    in_trend_signals = setup.get_in_trend_signals(
        htf1_trend=data['htf1_trend'], htf2_trend=data['htf2_trend']
    )
    assert in_trend_signals[-1]['trigger_candle'] == data['fa_buy_candles'][-1]


def test_fa_sell():
    data = SETUP_DATA
    setup = UltimateSetups(
        candles=data['fa_sell_candles'],
        buy_levels=data['buy_levels'],
        sell_levels=data['sell_levels'],
        pivot_lookback=data['pivot_lookback'],
        fo_lookback=data['fo_lookback']
    )
    signals = setup.get_signals()
    assert signals[-1]['trigger_candle'] == data['fa_sell_candles'][-1]
    
    in_trend_signals = setup.get_in_trend_signals(
        htf1_trend=data['htf1_trend'], htf2_trend=data['htf2_trend']
    )
    assert in_trend_signals[-1]['trigger_candle'] == data['fa_sell_candles'][-1]

