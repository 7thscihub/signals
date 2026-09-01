
class TradeSetup:
    '''
    Converts a signal into a complete trade setup with take profit levels (TP)
    and stop loss levels (SL).

    Parameters:

        signal: signal is a dictionary with a trigger candle and the lookback_hl.
                The lookback hl is the high or lowest point in the
                immediate lookback range that includes the trigger candle.
                The lookback_hl is used to set the stop loss for the trade 
                {lookback_hl: int, trigger_candle{tohlcvt}}
        tp1_rrr: The risk to reward ratio of the first take profit target.
        tp2_rrr: The risk to reward ratio of the second take profit target.
        sl_pading: The room beyond the signal high or low given to avoid by 
                    fakeouts is provided in percentage_as_a_fraction 10% as 0.1

    '''
    def __init__(self, signal, tp1_rrr=None, tp2_rrr=None, sl_padding=None):
        self._tp1_rrr = tp1_rrr
        self._tp2_rrr = tp2_rrr
        self._sl_padding = sl_padding
        self._signal = signal
        self._lookback_hl = signal["lookback_hl"]
        self._trigger_candle = signal["trigger_candle"]
        self._entry_price = signal["trigger_candle"]["close"]
        self._signal_time = signal["trigger_candle"]["time"]
        self._interval = signal['interval']

    @property
    def entry_price(self):
        return self._entry_price

    @property
    def signal_time(self):
        return self._signal_time

    @property
    def trade_direction(self):
        signal_type = self._signal["signal_type"]
        if "buy" in signal_type:
            return "buy"
        if "sell" in signal_type:
            return "sell"

    @property
    def tp1_rrr(self):
        if self._tp1_rrr is None:
            raise MissingRRRSError(
                f"Provide TP1 risk-reward ratio for {self._signal}"
            )
        return self._tp1_rrr
        
    @property
    def tp2_rrr(self):
        if self._tp2_rrr is None:
            raise MissingRRRSError(
                f"Provide TP2 risk-reward ratio for {self._signal}"
            )
        return self._tp2_rrr

    @property
    def sl_padding(self):
        if self._sl_padding is None:
            return 0
        return self._sl_padding

    def sell_sl(self):
        lookback_high = self._lookback_hl
        return lookback_high + (self.sl_padding * lookback_high)

    def buy_sl(self):
        lookback_low = self._lookback_hl
        return lookback_low - (self.sl_padding * lookback_low)


class BuyTrade(TradeSetup):
    def __init__(self, signal, tp1_rrr=3, tp2_rrr=10, sl_padding=0.01):
        super().__init__(signal, tp1_rrr, tp2_rrr, sl_padding)

    def percentage_risk(self):
        return (self._entry_price - self.buy_sl()) / self._entry_price * 100

    def tp1_percentage_profit(self):
        return self.tp1_rrr * self.percentage_risk()

    def percentage_profit(self):
        return self.tp2_rrr * self.percentage_risk()

    def tp1(self):
        return self._entry_price + (self.tp1_percentage_profit() * self._entry_price / 100)

    def tp2(self):
        return self._entry_price + (self.percentage_profit() * self._entry_price / 100)

    def trade_details(self):
        if self.trade_direction != "buy":
            return None
        trade_signal = self._signal | {
            "trigger_time": self.signal_time,
            "entry_price": self.entry_price,
            "sl": self.buy_sl(),
            "tp1": self.tp1(),
            "tp2": self.tp2(),
            "direction": "buy",
            "interval": self._interval
        }
        return trade_signal


class SellTrade(TradeSetup):
    def __init__(self, signal, tp1_rrr=3, tp2_rrr=10, sl_padding=0.01):
        super().__init__(signal, tp1_rrr, tp2_rrr, sl_padding)

    def percentage_risk(self):
        return (self.sell_sl() - self._entry_price) / self._entry_price * 100

    def tp1(self):
        perc_profit = self.tp1_rrr * self.percentage_risk()
        tp = self._entry_price - (perc_profit * self._entry_price / 100)
        return tp

    def tp2(self):
        perc_profit = self.tp2_rrr * self.percentage_risk()
        tp = self._entry_price - (perc_profit * self._entry_price / 100)
        return tp

    def trade_details(self):
        if self.trade_direction != "sell":
            return None
        trade_signal = self._signal | {
            "trigger_time": self.signal_time,
            "entry_price": self.entry_price,
            "sl": self.sell_sl(),
            "tp1": self.tp1(),
            "tp2": self.tp2(),
            "direction": "sell",
            "interval": self._interval
        }
        return trade_signal


def get_trade(signal, tp1_rrr=3, tp2_rrr=10, sl_padding=0.01):
    """
    Get trade details based on the trade signal provided.

    Param:
        signal: trade signal.
        tp1_rrr: Risk-reward ratio for the first take profit.
        tp2_rrr: Risk-reward ratio for the second take profit.
        sl_padding: Padding for the stop loss.

    return: Dictionary containing trade details or None if no valid trade.
    """
    trade_details = {}
    if signal is None:
        return None
    if buy_trade := BuyTrade(
        signal, tp1_rrr, tp2_rrr, sl_padding
        ).trade_details():
        trade_details.update(buy_trade)

    if sell_trade := SellTrade(
        signal, tp1_rrr, tp2_rrr, sl_padding
        ).trade_details():
        trade_details.update(sell_trade)

    return trade_details


def get_prev_trades(prev_signals, tp1_rrr=3, tp2_rrr=10, sl_padding=0.01):
    prev_trades = []
    if not prev_signals:
        return None
    for signal in prev_signals:
        trade_details = get_trade(signal, tp1_rrr, tp2_rrr, sl_padding)
        prev_trades.append(trade_details)
    return prev_trades or None


class MissingRRRSError(Exception):
    def __init__(self, message):
        message = message or 'missing risk to reward ratio'
        super().__init__(message)


