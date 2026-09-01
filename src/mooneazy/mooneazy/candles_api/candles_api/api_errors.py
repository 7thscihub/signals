
class YahooAPIError(Exception):
    def __init__(self, message=None):
        self.message = message or f"Yahoo API failed to fetch candles!!"
        super().__init__(self.message)
        

class BinanceAPIError(Exception):
    def __init__(self, message=None):
        self.message = message or f"Binance API failed to fetch candles!!"
        super().__init__(self.message)


class CandleCreationFailed(Exception):
    def __init__(self, message=None):
        self.message = message or 'Failed to build candles from API data.'
        super().__init__(self.message)


class CandleFetchingFailed(Exception):
    def __init__(self, message=None):
        self.message = message or 'Failed to get candles from API.'
        super().__init__(self.message)


class ResponseQuantityExceeded(Exception):
    def __init__(self, message=None):
        self.message = message or 'Request Quantity argument Exceeds response daata.'
        super().__init__(self.message)


