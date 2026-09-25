from unittest.mock import patch
import pytest
from pydantic import ValidationError
from mooneazy.trading import results

from .results_data import (
    CANDLES,
    SIGNAL_DATA,
    UPDATED_SIGNAL_DATA,
    SIGNAL_DICT,
    UPDATED_SIGNAL_DICT,
    SIGNALS,
    UPDATED_RESULTS,
)


# ---------------------------------------------------------------------------
# get_signal_candles
# ---------------------------------------------------------------------------


def test_get_signal_candles():
    with patch(
        'mooneazy.candles_api.candles_api.api.get_candles',
        return_value=CANDLES,
    ) as mock_get_candles:

        result = results.get_signal_candles(
            symbol='BTCUSDT',
            interval='30m',
            start_time=1788768000000,
            limit=500,
        )

    assert result == CANDLES

    mock_get_candles.assert_called_once_with({
        'symbol': 'BTCUSDT',
        'interval': '30m',
        'start_time': 1788768000000,
        'limit': 500,
    })


def test_get_signal_candles_validates_arguments():
    with pytest.raises(ValidationError):
        results.get_signal_candles(
            symbol='BTCUSDT',
            interval='30m',
            start_time='not-an-int',
            limit=500,
        )


# ---------------------------------------------------------------------------
# get_signal_results
# ---------------------------------------------------------------------------


def test_get_signal_results_returns_updated_signal():
    with patch(
        'mooneazy.trading.results.get_signal_candles',
        return_value=CANDLES,
    ) as mock_get_candles, patch(
        'mooneazy.trading.tps.get_results',
        return_value=UPDATED_SIGNAL_DATA,
    ) as mock_get_results:

        result = results.get_signal_results(SIGNAL_DICT)

    assert result == UPDATED_SIGNAL_DICT

    mock_get_candles.assert_called_once_with(
        symbol='BTCUSDT',
        interval='30m',
        start_time=1788768000000,
        limit=500,
    )

    mock_get_results.assert_called_once_with(
        candles=CANDLES,
        signal_data=SIGNAL_DATA,
    )


def test_get_signal_results_returns_none_when_unchanged():
    with patch(
        'mooneazy.trading.results.get_signal_candles',
        return_value=CANDLES,
    ) as mock_get_candles, patch(
        'mooneazy.trading.results.tps.get_results',
        return_value=SIGNAL_DATA,
    ) as mock_get_results:

        result = results.get_signal_results(SIGNAL_DICT)

    assert result is None

    mock_get_candles.assert_called_once_with(
        symbol='BTCUSDT',
        interval='30m',
        start_time=1788768000000,
        limit=500,
    )

    mock_get_results.assert_called_once_with(
        candles=CANDLES,
        signal_data=SIGNAL_DATA,
    )


def test_get_signal_results_accepts_signal_dict():
    with patch(
        'mooneazy.trading.results.get_signal_candles',
        return_value=CANDLES,
    ), patch(
        'mooneazy.trading.tps.get_results',
        return_value=SIGNAL_DATA,
    ):

        result = results.get_signal_results(SIGNAL_DICT)

    assert result is None


def test_get_signal_results_does_not_mutate_input():
    original_signal = {
        '$id': 'signals_0003',
        'data': SIGNAL_DATA.copy(),
    }

    with patch(
        'mooneazy.trading.results.get_signal_candles',
        return_value=CANDLES,
    ), patch(
        'mooneazy.trading.tps.get_results',
        return_value=UPDATED_SIGNAL_DATA,
    ):

        results.get_signal_results(original_signal)

    assert original_signal == {
        '$id': 'signals_0003',
        'data': SIGNAL_DATA,
    }


def test_get_signal_results_rejects_invalid_signal():
    invalid_signal = {
        'data': {
            'symbol': 'BTCUSDT',
            # Required SignalModel fields are intentionally missing.
        }
    }

    with pytest.raises(ValidationError):
        results.get_signal_results(invalid_signal)


# ---------------------------------------------------------------------------
# get_new_results
# ---------------------------------------------------------------------------


def test_get_new_results_empty():
    result = results.get_new_results([])

    assert result == []


def test_get_new_results_returns_only_changed_signals():
    signal_1 = SIGNALS[0]
    signal_2 = SIGNALS[1]

    with patch(
        'mooneazy.trading.results.get_signal_results',
        side_effect=[
            UPDATED_RESULTS[0],
            None,
        ],
    ) as mock_get_signal_results:

        result = results.get_new_results([
            signal_1,
            signal_2,
        ])

    assert result == [
        UPDATED_RESULTS[0],
    ]

    assert mock_get_signal_results.call_count == 2

    mock_get_signal_results.assert_any_call(signal_1)
    mock_get_signal_results.assert_any_call(signal_2)


def test_get_new_results_returns_all_changed_signals():
    result_1 = {
        'data': {
            **SIGNAL_DATA,
            'tp1_status': 'success',
            'status': 'partial',
        }
    }

    result_2 = {
        'data': {
            **SIGNAL_DATA,
            'tp1_status': 'success',
            'tp2_status': 'success',
            'status': 'success',
        }
    }

    with patch(
        'mooneazy.trading.results.get_signal_results',
        side_effect=[
            result_1,
            result_2,
        ],
    ):

        result = results.get_new_results([
            SIGNALS[0],
            SIGNALS[1],
        ])

    assert result == [
        result_1,
        result_2,
    ]


def test_get_new_results_returns_empty_when_nothing_changed():
    with patch(
        'mooneazy.trading.results.get_signal_results',
        return_value=None,
    ):

        result = results.get_new_results(SIGNALS)

    assert result == []


def test_get_new_results_calls_get_signal_results_for_every_signal():
    with patch(
        'mooneazy.trading.results.get_signal_results',
        return_value=None,
    ) as mock_get_signal_results:

        results.get_new_results(SIGNALS)

    assert mock_get_signal_results.call_count == len(SIGNALS)

    for signal in SIGNALS:
        mock_get_signal_results.assert_any_call(signal)


def test_get_new_results_rejects_non_list():
    with pytest.raises(ValidationError):
        results.get_new_results(SIGNAL_DICT)
