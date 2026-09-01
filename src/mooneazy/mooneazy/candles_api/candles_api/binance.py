import requests
from mooneazy.candles_api.candles_api import api_errors


def get_candles_from_params(params: dict)->list[dict]:
	"""
	Fetch candlestick data from Binance API with either specified 
	start time and end time or providing the limit(number of recent candles to fetch).
	
	"""
	base_url = "https://fapi.binance.com"
	endpoint = "/fapi/v1/klines"
	url = f"{base_url}{endpoint}"
	try:
		response = requests.get(url, params=params).json()
	except Exception as e:
		raise api_errors.CandleFetchingFailed(
			f"""
			Binance API failed to fetch candles from parameters
			Parameters: {params}
			Error: {e}
			"""
		)
	
	# print(f'from binance: {response}')
	candles = []
	# exclude the last unclosed/open candle
	for data in response[:-1]: 
		try:
			keys = ['time', 'open', 'high', 'low', 'close', 'volume', 'end_time']
			values = [float(i) for i in data[:7]]
			candle = dict(zip(keys, values))
			candles.append(candle)
		except Exception as e:
			raise api_errors.CandleCreationFailed(
				f"""
				parameters: {params}'
				data: {data} 
				error: {e}
				"""
			)
	return candles


def get_parameters(parameters):
		# print(f'from binance: params{parameters}')
		if not parameters['symbol']:
			raise api_errors.MissingParameters('symbol')
		if not parameters['interval']:
			raise api_errors.MissingParameters('interval')
		if not 'start_time' in parameters and not 'limit' in parameters:
			raise api_errors.MissingParameters(f'provide either limit or start time')

		return parameters


def get_candles(parameters)->list[dict]:
	"""returns candles from binance api exclusding the unclosed candle"""
	request_params = get_parameters(parameters)
	return get_candles_from_params(request_params)
	

if __name__ == "__main__":
	parameters = {
	'interval': "30m",
	'symbol': "XAUUSDT",
	'limit': 20
	}
	candles = get_candles(parameters=parameters)
	print(candles)

