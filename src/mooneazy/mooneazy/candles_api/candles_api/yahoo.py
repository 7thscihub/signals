import time
import json
from typing import Tuple, List, Dict
import requests
from mooneazy.candles_api.candles_api import api_errors


def get_start_time_end_time(parameters: dict) -> Tuple[str, str, int, int, int]:
    """Calculate symbol, interval, start, end, and limit for Yahoo requests."""
    end_time = int(time.time())

    # Accept legacy and new parameter names
    interval = parameters.get("interval") or parameters.get("period") or "1d"
    limit = parameters.get("limit") or parameters.get("quantity") or 1
    symbol = parameters.get("symbol") or parameters.get("ticker") or "GC=F"

    try:
        limit = int(limit)
    except Exception:
        limit = 1

    # Determine multiplier in seconds
    if interval.endswith("m") and interval[:-1].isdigit():
        minutes = int(interval[:-1])
        multiplier = minutes * 60
    elif interval.endswith("h") and interval[:-1].isdigit():
        hours = int(interval[:-1])
        multiplier = hours * 3600
    elif interval.endswith("d") and interval[:-1].isdigit():
        days = int(interval[:-1])
        multiplier = days * 24 * 3600
    else:
        multiplier = 24 * 3600  # default to 1 day

    # Buffer to ensure enough historical points (larger buffer for intraday)
    buffer_factor = 2 if "d" in interval else 10
    total_seconds_back = int(limit * multiplier * buffer_factor)

    start_time = end_time - total_seconds_back
    return symbol, interval, start_time, end_time, limit


def get_candles(parameters: dict) -> List[Dict]:
    """Fetch historical candlestick data from Yahoo Finance using requests.

    Returns a list of dicts with keys: time, open, high, low, close, volume.
    """
    symbol, interval, start_time, end_time, limit = get_start_time_end_time(parameters)

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"period1": start_time, "period2": end_time, "interval": interval}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        raw = resp.json()
    except requests.RequestException as e:
        raise api_errors.YahooAPIError(f"Network error when contacting Yahoo Finance: {e}") 
    except ValueError as e:
        raise api_errors.YahooAPIError(f"Invalid JSON from Yahoo Finance: {e}") 

    chart = raw.get("chart")
    if not chart or not chart.get("result"):
        raise api_errors.YahooAPIError("Malformed response from Yahoo Finance: missing chart/result")

    result = chart["result"][0]
    timestamps = result.get("timestamp") or []
    indicators = result.get("indicators", {})
    quote_list = indicators.get("quote") or []
    if not quote_list:
        raise api_errors.YahooAPIError("Malformed response from Yahoo Finance: missing indicators.quote")

    quote = quote_list[0]
    opens = quote.get("open", [])
    highs = quote.get("high", [])
    lows = quote.get("low", [])
    closes = quote.get("close", [])
    volumes = quote.get("volume", [])

    # Build candles defensively
    length = min(len(timestamps), len(opens), len(closes))
    candles = []
    for i in range(length):
        if opens[i] is None or closes[i] is None:
            continue
        candles.append({
            "time": timestamps[i],
            "open": opens[i],
            "high": highs[i] if i < len(highs) else None,
            "low": lows[i] if i < len(lows) else None,
            "close": closes[i],
            "volume": volumes[i] if i < len(volumes) else None,
        })

    if limit <= 0:
        return []
    return candles[-limit:-1]


if __name__ == "__main__":
    # Quick local test (adjust parameters as needed)
    params = {"symbol": "GC=F", "interval": "4h", "limit": 100}
    try:
        candles = get_candles(params)
        print(json.dumps(candles, indent=2))
        print(f"--- Retrieved {len(candles)} Candles ---")
    except Exception as e:
        print("Error:", e)
