
class MissingPivotData(Exception):
    def __init__(self):
        self.message = 'The pivot node is missing price and time data'

        super().__init__(self.message)


class ProvideHTFCandles(Exception):
    def __init__(self):
        self.message = (
            'You need to provide higher timeframe candles'
            'to validate the trend of the trade'
        )
        super().__init__(self.message)


class ProvideRequestArgs(Exception):
    def __init__(self,):
        self.message = (
            'Provide request arguments'
        )
        super().__init__(self.message)


class ProvideSetupCandles(Exception):
    def __init__(self, *args):
        self.message = (
            'Provide Both high timeframe Candles'
            'and trade timeframe candles for the setup'
        )
        super().__init__(*args)


class ProvideFastAndSlowEmaValues(Exception):
    def __init__(self, message):
        
        self.message = (
            'Provide Both high timeframe Candles'
            'and trade timeframe candles for the setup'
        )
        error_message = message or self.message
        super().__init__(error_message)

        


