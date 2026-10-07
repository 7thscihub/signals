
class Configs:
    def __init__(self):
        # supported symbols
        self.supported_symbols = ['BTCUSDT', 'ETHUSDT', 'XAUUSDT']

        # trading candles parameters
        self.default_limit = 500
        # lookback settings
        self.fo_lookback = 5
        self.ult_pivot_lookback = 30
        self.pullback_lookback_values = [5, 10]
        self.breakout_lookback = 5
                
        # indicator settings
        self.ema_cross_periods = [8, 20]
        self.hull_period = 55

        # tp rrrs
        self.pullback_tp_rrrs = [2, 5]
        self.breakout_tp_rrrs = [2, 5]
        self.ult_tp_rrrs = [1.5, 3]
        self.sl_padding = 0.001

        # breakout settings
        self.min_opposite_candles = 2
        self.min_score = 6

        # heads and shoulder pullback setting
        self.hs_pivot_lookback = 5
        self.hs_fo_lookback = 3
        self.hs_tp_rrrs = (2, 5)
        self.sr_fib = 0.8
        self.supported_scalping_intervals = {
            'engulfing_breakout': ['15m', '30m',],
            'ult_setups': ['30m'],
            'pullback_strategy': ['15m'],
            'heads_and_shoulders': ['30m']
        }
        self.scalping_trend_intervals =['4h', '1d', '1w']
        self.ult_setups_configs = {
            'intervals': ['30m'],
            'pivot_lookback': 30,
            'fo_lookback': 5,
            'tp_rrrs': (1.5, 3),
            'sl_padding': 0.001
        }
        self.engulfing_breakout_configs = {
            'fo_lookback': 5,
            'ema_cross_periods': (8, 20),
            'min_opposite_candles': 2,
            'hull_period': 55,
            'min_score': 8,
            'tp_rrrs': (2, 5),
            'sl_padding': 0.001
        }
        self.lookback_configs = {
            'intervals': ['15m', '30m'],
            'lookback_values': (5, 10),
            'fib_level': 0.3,
            'tp_rrrs': (2, 5),
            'sl_padding': 0.001,
        }
        self.heads_and_shoulders_configs = {
            'intervals': ['30m'],
            'fo_lookback': 3,
            'sr_level': 0.8,
            'pivot_lookback': 5,
            'tp_rrrs': (2, 5),
        }


