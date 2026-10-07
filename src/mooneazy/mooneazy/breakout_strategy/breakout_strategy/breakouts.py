import json
from pydantic import validate_call
from . import breakout
from .emas import EmaCross
from .hma import BreakoutHMA
from .models import BreakoutConfigs
from . import util


class Breakouts:
    @validate_call
    def __init__(self, 
            candles:list[dict], 
            trend:str,
            interval:str,
            configs: BreakoutConfigs = BreakoutConfigs()
        ):
        self._trading_tf_candles = candles
        self.configs = configs
        self.trend = trend
        self.interval = interval

        self.fast_ema_period = min(configs.ema_cross_periods)
        self.slow_ema_period = max(configs.ema_cross_periods)
        
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
            period=self.configs.hull_period,
            lookback_left=self.configs.fo_lookback
        ).get_all_hmas()

    def get_ema_crosses(self):
        return EmaCross(
            candles=self._trading_tf_candles,
            fast_ema_period=self.fast_ema_period,
            slow_ema_period=self.slow_ema_period
        ).get_crosses()
    
    def get_breakout_slices(self, candle_index) -> dict[str:list]:
        kwargs = {
            'breakout_candles': self._trading_tf_candles,
            'fast_ema_values': self._fast_ema_values,
            'slow_ema_values': self._slow_ema_values,
            'hull_values': self._hull_values
        }
        return util.get_lookback_slices(
            candle_index=candle_index,
            lookback=self.configs.fo_lookback,
            **kwargs
        )
    
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
                min_opposite_candles=self.configs.min_opposite_candles
            ).get_in_trend_breakout(
                min_score=self.configs.min_score, 
                trend=self.trend
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
                interval=self.interval,
                tp_rrrs=self.configs.tp_rrrs,
                sl_padding=self.configs.sl_padding,
                score=signal['score']
            )
            trade_signals.append(trade_signal)
        return trade_signals

    def get_latest_trade_signal(self):
        trade_signals = self.get_trade_signals()
        if not trade_signals:
            return None
        return trade_signals[-1]

