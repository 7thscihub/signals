from unittest.mock import patch

from .tps_data import (
    SIGNAL_DATA,
    CANDLES_NO_HIT,
    CANDLES_TP1,
    CANDLES_SL,
    CANDLES_TP1_THEN_TP2,
    CANDLES_SL_THEN_TP1,
    CANDLES_BOTH_TOUCHED,
    LOWER_TIMEFRAME_CANDLES_TP,
    LOWER_TIMEFRAME_CANDLES_SL,
    LOWER_TIMEFRAME_CANDLES_BOTH,
    TP_DATA,
    STOP_LOSS,
    TP_PENDING,
    TP_SUCCESS,
    TP_FAILED
)
from mooneazy.trading.models import SignalData 
from mooneazy.trading.tps import (
    touches,
    get_signal_candles,
    collect_signal_tps,
    get_interval_minutes,
    is_stopped_lower_timeframe,
    resolve_with_lower_time_frame,
    is_stopped_out,
    get_signal_status,
    get_results
)


def test_signal_data():
    signal = SignalData(**SIGNAL_DATA)

    assert signal.symbol == 'BTCUSDT'
    assert signal.interval == '30m'
    assert signal.time == 1000
    assert signal.signal_type == 'sfp_buy'
    assert signal.entry_price == 100.0
    assert signal.sl == 95.0
    assert signal.tp1 == 105.0
    assert signal.tp2 == 110.0
    assert signal.tp1_status == 'pending'
    assert signal.tp2_status == 'pending'
    assert signal.status == 'pending'


def test_touches():
    candle = {
        'high': 105,
        'low': 95
    }

    assert touches(candle, 105) is True
    assert touches(candle, 100) is True
    assert touches(candle, 95) is True
    assert touches(candle, 106) is False
    assert touches(candle, 94) is False


def test_get_signal_candles():
    expected_candles = CANDLES_TP1

    with patch(
        'mooneazy.candles_api.candles_api.api.get_candles',
        return_value=expected_candles
    ) as mock_get_candles:
        result = get_signal_candles(
            symbol='BTCUSDT',
            interval='1m',
            start_time=1000,
            limit=30
        )

    assert result == expected_candles

    mock_get_candles.assert_called_once_with({
        'interval': '1m',
        'start_time': 1000,
        'symbol': 'BTCUSDT',
        'limit': 30
    })


def test_collect_signal_tps():
    result = collect_signal_tps(SIGNAL_DATA)

    assert result == TP_DATA


def test_collect_signal_tps_skips_missing_targets():
    signal_data = {
        'tp1': 105.0,
        'tp1_status': 'pending',
        'tp2': None,
        'tp2_status': 'pending',
        'tp3_status': 'pending'
    }

    result = collect_signal_tps(signal_data)

    assert result == {
        'tp1': {
            'target': 105.0,
            'status': 'pending'
        }
    }


def test_get_interval_minutes():
    assert get_interval_minutes('1m') == 1
    assert get_interval_minutes('5m') == 5
    assert get_interval_minutes('15m') == 15
    assert get_interval_minutes('30m') == 30
    assert get_interval_minutes('1h') == 60
    assert get_interval_minutes('2h') == 120
    assert get_interval_minutes('1d') == 1440


def test_get_interval_minutes_unsupported_interval():
    try:
        get_interval_minutes('1w')
        assert False
    except KeyError as error:
        assert str(error) == "'Unsupported interval: 1w'"


def test_is_stopped_lower_timeframe_tp_first():
    stop_loss = {
        'value': 95.0
    }

    tp = {
        'target': 105.0
    }

    result = is_stopped_lower_timeframe(
        LOWER_TIMEFRAME_CANDLES_TP,
        stop_loss,
        tp
    )

    assert result is False


def test_is_stopped_lower_timeframe_sl_first():
    stop_loss = {
        'value': 95.0
    }

    tp = {
        'target': 105.0
    }

    result = is_stopped_lower_timeframe(
        LOWER_TIMEFRAME_CANDLES_SL,
        stop_loss,
        tp
    )

    assert result is True


def test_is_stopped_lower_timeframe_both_touched():
    stop_loss = {
        'value': 95.0
    }

    tp = {
        'target': 105.0
    }

    result = is_stopped_lower_timeframe(
        LOWER_TIMEFRAME_CANDLES_BOTH,
        stop_loss,
        tp
    )

    assert result is False


def test_is_stopped_lower_timeframe_no_hit():
    candles = [
        {
            'time': 1000,
            'high': 103,
            'low': 98
        }
    ]

    stop_loss = {
        'value': 95.0
    }

    tp = {
        'target': 105.0
    }

    result = is_stopped_lower_timeframe(
        candles,
        stop_loss,
        tp
    )

    assert result is False


def test_resolve_with_lower_time_frame():
    with patch(
        'mooneazy.trading.tps.get_signal_candles',
        return_value=LOWER_TIMEFRAME_CANDLES_TP
    ) as mock_get_candles:

        result = resolve_with_lower_time_frame(
            signal_data=SIGNAL_DATA,
            stop_loss=STOP_LOSS,
            tp={
                'target': 105.0
            }
        )

    assert result is False

    mock_get_candles.assert_called_once_with(
        symbol='BTCUSDT',
        interval='1m',
        start_time=1000,
        limit=30
    )


def test_is_stopped_out_no_stop_loss_time():
    stop_loss = {
        'value': 95.0,
        'time': None
    }

    result = is_stopped_out(
        stop_loss=stop_loss,
        tp=TP_SUCCESS,
        signal_data=SIGNAL_DATA
    )

    assert result is False


def test_is_stopped_out_no_tp_time():
    stop_loss = {
        'value': 95.0,
        'time': 1000
    }

    tp = {
        'target': 105.0,
        'time': None
    }

    result = is_stopped_out(
        stop_loss=stop_loss,
        tp=tp,
        signal_data=SIGNAL_DATA
    )

    assert result is True


def test_is_stopped_out_stop_loss_before_tp():
    stop_loss = {
        'value': 95.0,
        'time': 1000
    }

    tp = {
        'target': 105.0,
        'time': 1060
    }

    result = is_stopped_out(
        stop_loss=stop_loss,
        tp=tp,
        signal_data=SIGNAL_DATA
    )

    assert result is True


def test_is_stopped_out_tp_before_stop_loss():
    stop_loss = {
        'value': 95.0,
        'time': 1060
    }

    tp = {
        'target': 105.0,
        'time': 1000
    }

    result = is_stopped_out(
        stop_loss=stop_loss,
        tp=tp,
        signal_data=SIGNAL_DATA
    )

    assert result is False


def test_is_stopped_out_same_time():
    stop_loss = {
        'value': 95.0,
        'time': 1000
    }

    tp = {
        'target': 105.0,
        'time': 1000
    }

    with patch(
        'mooneazy.trading.tps.resolve_with_lower_time_frame',
        return_value=True
    ) as mock_resolve:

        result = is_stopped_out(
            stop_loss=stop_loss,
            tp=tp,
            signal_data=SIGNAL_DATA
        )

    assert result is True
    mock_resolve.assert_called_once()


def test_get_signal_status_no_tps():
    assert get_signal_status({}) == 'pending'


def test_get_signal_status_all_pending():
    tps = {
        'tp1': {'status': 'pending'},
        'tp2': {'status': 'pending'}
    }

    assert get_signal_status(tps) == 'pending'


def test_get_signal_status_all_success():
    tps = {
        'tp1': {'status': 'success'},
        'tp2': {'status': 'success'}
    }

    assert get_signal_status(tps) == 'success'


def test_get_signal_status_partial():
    tps = {
        'tp1': {'status': 'success'},
        'tp2': {'status': 'pending'}
    }

    assert get_signal_status(tps) == 'partial'


def test_get_signal_status_failed():
    tps = {
        'tp1': {'status': 'failed'},
        'tp2': {'status': 'pending'}
    }

    assert get_signal_status(tps) == 'failed'


def test_get_signal_status_success_and_failed():
    tps = {
        'tp1': {'status': 'success'},
        'tp2': {'status': 'failed'}
    }

    assert get_signal_status(tps) == 'partial'


def test_get_results_tp_pending():
    result = get_results(
        CANDLES_NO_HIT,
        SIGNAL_DATA
    )

    assert result['tp1_status'] == 'pending'
    assert result['tp2_status'] == 'pending'
    assert result['status'] == 'pending'


def test_get_results_tp_success():
    result = get_results(
        CANDLES_TP1,
        SIGNAL_DATA
    )

    assert result['tp1_status'] == 'success'
    assert result['tp2_status'] == 'pending'
    assert result['status'] == 'partial'


def test_get_results_stop_loss_before_tp():
    result = get_results(
        CANDLES_SL_THEN_TP1,
        SIGNAL_DATA
    )

    assert result['tp1_status'] == 'failed'
    assert result['tp2_status'] == 'failed'
    assert result['status'] == 'failed'


def test_get_results_multiple_tps():
    result = get_results(
        CANDLES_TP1_THEN_TP2,
        SIGNAL_DATA
    )

    assert result['tp1_status'] == 'success'
    assert result['tp2_status'] == 'success'
    assert result['status'] == 'success'


def test_get_results_preserves_signal_data():
    result = get_results(
        CANDLES_NO_HIT,
        SIGNAL_DATA
    )

    assert result['symbol'] == SIGNAL_DATA['symbol']
    assert result['interval'] == SIGNAL_DATA['interval']
    assert result['time'] == SIGNAL_DATA['time']
    assert result['entry_price'] == SIGNAL_DATA['entry_price']
    assert result['sl'] == SIGNAL_DATA['sl']
    assert result['tp1'] == SIGNAL_DATA['tp1']
    assert result['tp2'] == SIGNAL_DATA['tp2']
