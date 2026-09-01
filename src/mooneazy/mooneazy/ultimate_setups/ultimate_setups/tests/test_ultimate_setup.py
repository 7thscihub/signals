from tests.test_data import setup_data
from ultimate_setups.ultimate_setups.strategies.ultimate_setups import UltimateSetups 


def test_sfp():
    data = setup_data.setup_data
    setup = UltimateSetups(
        candles=data['sfp_buy_candles'],
        buy_levels=data['buy_levels'],
        sell_levels=data['sell_levels'],
        pivot_lookback=data['pivot_lookback'],
        fo_lookback=data['fo_lookback']
    )
    signals = setup.get_signals()
    assert signals is True
    