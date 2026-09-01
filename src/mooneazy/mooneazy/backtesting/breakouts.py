from .mooneazy.breakout_strategy.breakout_strategy import breakout
from .mooneazy.breakout_strategy.breakout_strategy.emas import EmaCross
from .mooneazy.breakout_strategy.breakout_strategy.hma import BreakoutHMA
from .mooneazy.breakout_strategy.breakout_strategy import signals
from .mooneazy.backtesting import breakout_util as util


class Breakouts:
    def __init__(self, 
            trading_tf_candles, 
            fo_lookback, 
            fast_ema_period, 
            slow_ema_period,
            hull_period,
            min_opposite_candles,
        ):
        self._trading_tf_candles = trading_tf_candles
        self.fo_lookback = fo_lookback
        self.fast_ema_period = fast_ema_period
        self.slow_ema_period = slow_ema_period
        self.hull_period = hull_period
        self.min_opposite_candles = min_opposite_candles
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
        candles = self._trading_tf_candles
        for i in range(100, len(candles)):
            slices = self.get_breakout_slices(candle_index=i)
            valid_breakout = breakout.BreakOut(
                breakout_candles=slices['breakout_candles'],
                fast_ema_values=slices['fast_ema_values'],
                slow_ema_values=slices['slow_ema_values'],
                hull_values=slices['hull_values'],
                min_opposite_candles=self.min_opposite_candles
            ).get_in_trend_breakout(min_score=6, htf1_trend='buy', htf2_trend='sell')
            if valid_breakout:
                breakouts.append(candles[i])

        return breakouts
    
    def get_trade_signals(self):
        trade_signals = []
        candles = self._trading_tf_candles
        for i in range(100, len(candles)):
            signal = signals.get_breakout_trade_signal(
                trading_tf_candles=candles[:i + 1],
                htf_trends=('buy', 'buy'),
                lookback_left=self.fo_lookback,
                min_opposite_candles=self.min_opposite_candles,
                ema_cross_periods=(8, 20),
                hull_period=55,
                interval='15m',
                tp_rrrs=(2, 5),
                sl_padding=0.001
            )
            if signal:
                trade_signals.append(signal)
        return trade_signals or None
