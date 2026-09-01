import json
from . import breakout
from .emas import EmaCross
from .hma import BreakoutHMA
from . import util


class Breakouts:
    def __init__(self, 
            trading_tf_candles, 
            fo_lookback=5, 
            ema_cross_periods=(8, 20),
            hull_period=55,
            min_opposite_candles=2,
            min_score=6,
            tp_rrrs=(2, 5),
            interval='30m',
            htf_trends=('buy', 'sell'),
            sl_padding=0.001
        ):
        self._trading_tf_candles = trading_tf_candles
        self.fo_lookback = fo_lookback
        self.ema_cross_periods = ema_cross_periods
        self.fast_ema_period = min(ema_cross_periods)
        self.slow_ema_period = max(ema_cross_periods)
        self.hull_period = hull_period
        self.min_opposite_candles = min_opposite_candles
        self._min_score = min_score
        self._tp_rrrs = tp_rrrs
        self._interval = interval
        self._htf_trends = htf_trends
        self._sl_padding = sl_padding
        self._fast_ema_values = self.fast_ema_values()
        self._slow_ema_values = self.slow_ema_values()
        self._hull_values = self.hull_values()
        
        
    def fast_ema_values(self):
        return EmaCross(
            candles=self._trading_tf_candles,
            fast_ema_period=self.fast_ema_period,
            slow_ema_period=self.slow_ema_period
        ).get_emas(self.fast_ema_period)

    def slow_ema_values(self):
        return EmaCross(
            candles=self._trading_tf_candles,
            fast_ema_period=self.fast_ema_period,
            slow_ema_period=self.slow_ema_period
        ).get_emas(self.slow_ema_period)

    def hull_values(self):
        return BreakoutHMA(
            indicator_candles=self._trading_tf_candles,
            period=self.hull_period,
            lookback_left=self.fo_lookback
        ).get_all_hmas()

    def get_ema_crosses(self):
        crosses = EmaCross(
            candles=self._trading_tf_candles,
            fast_ema_period=self.fast_ema_period,
            slow_ema_period=self.slow_ema_period
        ).get_crosses()
        return crosses
    
    def get_breakout_slices(self, candle_index) -> dict[str:list]:
        kwargs = {
            'breakout_candles': self._trading_tf_candles,
            'fast_ema_values': self._fast_ema_values,
            'slow_ema_values': self._slow_ema_values,
            'hull_values': self._hull_values
        }
        slices_dict = util.get_lookback_slices(
            candle_index=candle_index,
            lookback=self.fo_lookback,
            **kwargs
        )
        return slices_dict
    
    def get_valid_breakouts(self):
            breakouts = []
            htf1_trend, htf2_trend = self._htf_trends
            candles = self._trading_tf_candles
            for i in range(100, len(candles)):
                slices = self.get_breakout_slices(candle_index=i)
                valid_breakout = breakout.BreakOut(
                    breakout_candles=slices['breakout_candles'],
                    fast_ema_values=slices['fast_ema_values'],
                    slow_ema_values=slices['slow_ema_values'],
                    hull_values=slices['hull_values'],
                    min_opposite_candles=self.min_opposite_candles
                ).get_in_trend_breakout(
                    min_score=self._min_score, htf1_trend=htf1_trend, htf2_trend=htf2_trend
                )
                if valid_breakout:
                    breakouts.append(valid_breakout)

            return breakouts

    def get_trade_signals(self):
        breakout_signals = self.get_valid_breakouts()
        if not breakout_signals:
            return None
        trade_signals = []
        for signal in breakout_signals:
            trade_signal = util.make_trade_signal(
                breakout_candle=signal['trigger_candle'],
                interval=self._interval,
                tp_rrrs=self._tp_rrrs,
                sl_padding=self._sl_padding,
                score=signal['score']
            )
            trade_signals.append(trade_signal)
        return trade_signals

    def get_latest_trade_signal(self):
        trade_signals = self.get_trade_signals()
        if not trade_signals:
            return None
        return trade_signals[-1]
    
        
        
