from datetime import datetime, timezone

def get_interval_in_seconds(interval):
    interval_value = int(interval[:-1])
    time_symbol = interval[-1].lower()
    interval_in_seconds = 0
    if time_symbol == 'm':
        interval_in_seconds = interval_value * 60
    if time_symbol == 'h':
        interval_in_seconds = interval_value * 3600
    if time_symbol == 'd':
        interval_in_seconds = interval_value * 3600 * 24
    if time_symbol == 'w':
        interval_in_seconds = interval_value * 3600 * 24 * 7
    return interval_in_seconds


def is_active_signal(signal_time, interval):
    """
    Check if the signal trigger time is within the last uptime duration.
    Multiplies the interval by 2 to ensure the signal stays valid 
    throughout the next candle since the signal time is the starting time of the candle.
    parameter:
        signal_time (unix_time): the trigger candle start time i.e time.
        interval: the interval of the candle.
    """
    
    # print(unix_to_utc(signal_time))
    uptime_duration_in_seconds = get_interval_in_seconds(interval) * 3
    current_time_in_seconds = datetime.now(timezone.utc).timestamp()
    signal_time_in_seconds = signal_time / 1000
    lapse_time = abs(current_time_in_seconds - signal_time_in_seconds)
    # print(f"{lapse_time} : {uptime_duration_in_seconds}")
    return lapse_time <= uptime_duration_in_seconds


def unix_to_utc(unix_timestamp):
    unix_timestamp = int(unix_timestamp)
    return datetime.fromtimestamp(
        unix_timestamp / 1000, tz=timezone.utc
    ).strftime('%Y-%m-%d %H:%M:%S')


