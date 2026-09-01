from mooneazy.candles_api.candles_api import api as candles_api
from mooneazy.pullback_strategy.pullback_strategy import signals as pullback_signals
from mooneazy.pullback_strategy.pullback_strategy.head_and_shoulder import HeadAndShoulder
from mooneazy.breakout_strategy.breakout_strategy import breakouts
from mooneazy.ultimate_setups.ultimate_setups import signals as ult_signals
from mooneazy.scripts.config import Configs
from mooneazy.scripts import htf_trend


class Analyze:
    def __init__(
            self, 
            symbol, 
            configs:object=None,
            htf1_candles:list[dict]=[], 
            htf2_candles:list[dict]=[], 
            m30_candles:list[dict]=[], 
            m15_candles:list[dict]=[],
            htf_trends:tuple=('buy', 'sell')
        ):
        self._symbol = symbol
        self._configs = configs or Configs()
        self._htf1_candles = htf1_candles or self.get_candles('4h', 500)
        self._htf2_candles = htf2_candles or self.get_candles('1d', 500)
        self._m30_candles = m30_candles or self.get_candles('30m', 500)
        self._m15_candles = m15_candles or self.get_candles('15m', 500)
        self._htf_trends = htf_trends or self.get_htf_trends()

    def get_htf_trends(self):
        fast_ema_period, slow_ema_period = self._configs.ema_cross_periods
        trends = htf_trend.get_htf_trends(
            htf1_candles=self._htf1_candles, 
            htf2_candles=self._htf2_candles,
            fast_ema_period=fast_ema_period,
            slow_ema_period=slow_ema_period
        )
        return trends

    def get_candles(self, interval, limit):
        parameters = {
            'symbol': self._symbol,
            'interval': interval,
            'limit': limit
        }
        return candles_api.get_candles(parameters=parameters)
    
    def get_pullback_signal(self)->dict[str, any] | None:
        configs = self._configs
        signals = pullback_signals.get_trade_signal(
            htf_candles = self._htf1_candles,
            trading_tf_candles = self._m15_candles,
            trading_interval = '15m',
            lookback_values = configs.pullback_lookback_values,
            fo_lookback = configs.fo_lookback,
            tp_rrrs = configs.pullback_tp_rrrs,
            sl_padding = configs.sl_padding
        )
        return signals
    
    def get_breakout_signals(self):
        # print(f"from analysis.analyze: symbol: {self._symbol}: htf_trends: {self._htf_trends}")
        configs = self._configs
        signals = []
        breakout_parameters = {
            'htf_trends': self._htf_trends,
            'fo_lookback': configs.breakout_lookback,
            'min_opposite_candles': configs.min_opposite_candles,
            'ema_cross_periods': configs.ema_cross_periods,
            'hull_period': configs.hull_period,
            'tp_rrrs': configs.breakout_tp_rrrs,
            'sl_padding': configs.sl_padding,
            'min_score': self._configs.min_score
        }
        m15_params = breakout_parameters | {
            'interval': '15m', 'trading_tf_candles': self._m15_candles
        }
        m30_params = breakout_parameters | {
            'interval': '30m', 'trading_tf_candles': self._m30_candles
        }
        m15_signal = breakouts.Breakouts(**m15_params).get_latest_trade_signal()
        m30_signal = breakouts.Breakouts(**m30_params).get_latest_trade_signal()

        if m15_signal:
            signals.append(m15_signal)
        if m30_signal:
            signals.append(m30_signal)
        return signals 

    def get_ult_signal(self):
        configs = self._configs
        signal = ult_signals.get_ult_signal( 
            htf1_candles=self._htf1_candles, 
            htf2_candles=self._htf2_candles, 
            trading_tf_candles=self._m30_candles, 
            pivot_lookback=configs.ult_pivot_lookback, 
            fo_lookback=configs.fo_lookback, 
            ema_cross_periods=configs.ema_cross_periods,
            tp_rrrs=configs.ult_tp_rrrs,
            sl_padding=configs.sl_padding,
            interval='30m'
        )
        return signal
    
    def get_hs_signal(self):
        trade_signals = HeadAndShoulder(
            candles=self._m30_candles, configs=self._configs
        ).latest_trade_signal()
        return trade_signals

    def get_signals(self):
        signals = []
        if breakout_signal := self.get_breakout_signals():
            signals.extend(breakout_signal)
        if ult_signal := self.get_ult_signal():
            signals.append(ult_signal)
        if pullback_signal := self.get_pullback_signal():
            signals.append(pullback_signal)
        if hs_signal := self.get_hs_signal():
            signals.append(hs_signal)

        if not signals:
            return None
        
        for signal in signals:
            signal['symbol'] = self._symbol
            signal['time'] = signal['trigger_candle']['time']
        return signals


def get_signals(supported_symbols=Configs().supported_symbols):
    signals = []
    for symbol in supported_symbols:
        if symbol_signals := Analyze(symbol).get_signals():
            signals.extend(symbol_signals)
    return signals or None


