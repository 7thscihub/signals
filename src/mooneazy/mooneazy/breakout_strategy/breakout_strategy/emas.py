class EMA:
    def __init__(self, candles, sma_period=14, ema_period=14):
        self.candles = candles
        self.sma_period = sma_period
        self.ema_period = ema_period

    def get_emas(self):
        candles = self.candles
        ema_values = self.calculate_emas()
        emas = []
        for candle, value in zip(reversed(candles), reversed(ema_values)):
            ema = {
                "time": candle["time"],
                "value": value
            }
            emas.insert(0, ema)
        return emas

    def calculate_emas(self):
        candles = self.candles
        sma_period = self.sma_period
        ema_period = self.ema_period

        data = [c["close"] for c in candles]
        ema_values = []
        for i in range(sma_period - 1):
            ema_values.append(float('nan'))

        multiplier = 2 / (ema_period + 1)

        sma = sum(data[:sma_period]) / sma_period
        ema_values.append(sma)

        for price in data[sma_period:]:
            ema = (price - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)

        return ema_values


class EmaCross:
    def __init__(self, candles, fast_ema_period, slow_ema_period):
        self.candles = candles
        self.fast_period = fast_ema_period
        self.slow_period = slow_ema_period
        self.sma_period = 14
        self.fast_emas = self.get_emas(period=self.fast_period)
        self.slow_emas = self.get_emas(period=self.slow_period)

    def get_emas(self, period):
        return EMA(self.candles, sma_period=self.sma_period, ema_period=period).get_emas()

    def get_fast_ema(self):
        period = self.fast_period
        return self.get_emas(period)[-1]

    def get_slow_ema(self):
        period = self.slow_period
        return self.get_emas(period)[-1]

    def is_bullish_cross(self):  
        current_fast, prev_fast = self.fast_emas[-1], self.fast_emas[-2]
        current_slow, prev_slow = self.slow_emas[-1], self.slow_emas[-2]
        return current_fast > current_slow and prev_fast < prev_slow
    
    def is_bearish_cross(self):
        current_fast, prev_fast = self.fast_emas[-1], self.fast_emas[-2]
        current_slow, prev_slow = self.slow_emas[-1], self.slow_emas[-2]
        return current_fast < current_slow and prev_fast > prev_slow
     
    def is_bullish(self):
        return self.get_fast_ema()['value'] > self.get_slow_ema()['value']

    def is_bearish(self):
        return self.get_fast_ema()['value'] < self.get_slow_ema()['value']

    def get_last_cross(self):
        fast_emas = self.get_emas(self.fast_period)
        slow_emas = self.get_emas(self.slow_period)
        for i in range(len(fast_emas) - 1, 0, -1):
            if fast_emas[i]["value"] > slow_emas[i]["value"] and fast_emas[i - 1]["value"] < slow_emas[i - 1]["value"]:
                return {"time": fast_emas[i]["time"], "direction": "buy"}
            
            if fast_emas[i]["value"] < slow_emas[i]["value"] and fast_emas[i - 1]["value"] > slow_emas[i - 1]["value"]:
                return{
                    "time": fast_emas[i]["time"],
                    "direction": "sell"
                }
        return None
    
    def get_crosses(self):
        fast_emas = self.get_emas(self.fast_period)
        slow_emas = self.get_emas(self.slow_period)
        crosses = []
        for i in range(len(fast_emas) - 1, 0, -1):
            if fast_emas[i]["value"] > slow_emas[i]["value"] and fast_emas[i - 1]["value"] < slow_emas[i - 1]["value"]:
                crosses.append({"time": fast_emas[i]["time"], "direction": "buy"})
            
            if fast_emas[i]["value"] < slow_emas[i]["value"] and fast_emas[i - 1]["value"] > slow_emas[i - 1]["value"]:
                crosses.append({"time": fast_emas[i]["time"], "direction": "sell"})
        return crosses           
    

def get_breakout_ema_values(indicator_candles, fast_ema=8, slow_ema=20, lookback=5):
    '''
    returns the ema values for the lookback candles

    Parameters:
        indicator_candles: a full set of candles preferably 500 necessary for calculating 
        standard indicators consistent with trading view

    '''

    fast_emas = EMA(candles=indicator_candles, ema_period=fast_ema).calculate_emas()[-lookback:]
    slow_emas = EMA(candles=indicator_candles, ema_period=slow_ema).calculate_emas()[-lookback:]
    return (fast_emas, slow_emas)


