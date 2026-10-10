from unittest.mock import MagicMock, call, patch
import pytest
from mooneazy.breakout_strategy.breakout_strategy import breakouts
from mooneazy.models.breakouts import BreakoutConfigs
from . import breakouts_data as data


@pytest.fixture
def configs():
    return BreakoutConfigs(
        fo_lookback=20,
        ema_cross_periods=(9, 21),
        hull_period=16,
        min_opposite_candles=2,
        min_score=6,
        tp_rrrs=(1, 2, 3),
        breakout_intervals=["30m", "15m"],
        sl_padding=0.001,
    )


@pytest.fixture
def instance(configs):
    with (
        patch.object(
            breakouts.Breakouts,
            "fast_ema_values",
            return_value=data.FAST_EMA_VALUES,
        ),
        patch.object(
            breakouts.Breakouts,
            "slow_ema_values",
            return_value=data.SLOW_EMA_VALUES,
        ),
        patch.object(
            breakouts.Breakouts,
            "hull_values",
            return_value=data.HULL_VALUES,
        ),
    ):
        return breakouts.Breakouts(
            candles=data.CANDLES,
            trend="bullish",
            interval="30m",
            configs=configs,
        )


def test_init_sets_attributes_and_periods(instance, configs):
    assert instance._trading_tf_candles == data.CANDLES
    assert instance.configs == configs
    assert instance.trend == "bullish"
    assert instance.interval == "30m"

    assert instance.fast_ema_period == 9
    assert instance.slow_ema_period == 21

    assert instance._fast_ema_values == data.FAST_EMA_VALUES
    assert instance._slow_ema_values == data.SLOW_EMA_VALUES
    assert instance._hull_values == data.HULL_VALUES


def test_fast_ema_values():
    ema_cross = MagicMock()
    ema_cross.get_emas.return_value = data.FAST_EMA_VALUES

    with patch.object(
        breakouts,
        "EmaCross",
        return_value=ema_cross,
    ) as mock_ema:
        obj = object.__new__(breakouts.Breakouts)

        obj._trading_tf_candles = data.CANDLES
        obj.fast_ema_period = 9
        obj.slow_ema_period = 21

        result = obj.fast_ema_values()

    mock_ema.assert_called_once_with(
        candles=data.CANDLES,
        fast_ema_period=9,
        slow_ema_period=21,
    )

    ema_cross.get_emas.assert_called_once_with(9)

    assert result == data.FAST_EMA_VALUES


def test_slow_ema_values():
    ema_cross = MagicMock()
    ema_cross.get_emas.return_value = data.SLOW_EMA_VALUES

    with patch.object(
        breakouts,
        "EmaCross",
        return_value=ema_cross,
    ) as mock_ema:
        obj = object.__new__(breakouts.Breakouts)

        obj._trading_tf_candles = data.CANDLES
        obj.fast_ema_period = 9
        obj.slow_ema_period = 21

        result = obj.slow_ema_values()

    mock_ema.assert_called_once_with(
        candles=data.CANDLES,
        fast_ema_period=9,
        slow_ema_period=21,
    )

    ema_cross.get_emas.assert_called_once_with(21)

    assert result == data.SLOW_EMA_VALUES


def test_hull_values(configs):
    hma = MagicMock()
    hma.get_all_hmas.return_value = data.HULL_VALUES

    with patch.object(
        breakouts,
        "BreakoutHMA",
        return_value=hma,
    ) as mock_hma:
        obj = object.__new__(breakouts.Breakouts)

        obj._trading_tf_candles = data.CANDLES
        obj.configs = configs

        result = obj.hull_values()

    mock_hma.assert_called_once_with(
        indicator_candles=data.CANDLES,
        period=configs.hull_period,
        lookback_left=configs.fo_lookback,
    )

    hma.get_all_hmas.assert_called_once_with()

    assert result == data.HULL_VALUES


def test_get_ema_crosses():
    ema_cross = MagicMock()
    ema_cross.get_crosses.return_value = data.EMA_CROSSES

    with patch.object(
        breakouts,
        "EmaCross",
        return_value=ema_cross,
    ) as mock_ema:
        obj = object.__new__(breakouts.Breakouts)

        obj._trading_tf_candles = data.CANDLES
        obj.fast_ema_period = 9
        obj.slow_ema_period = 21

        result = obj.get_ema_crosses()

    mock_ema.assert_called_once_with(
        candles=data.CANDLES,
        fast_ema_period=9,
        slow_ema_period=21,
    )

    ema_cross.get_crosses.assert_called_once_with()

    assert result == data.EMA_CROSSES


def test_get_breakout_slices(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = data.CANDLES
    obj.configs = configs
    obj._fast_ema_values = data.FAST_EMA_VALUES
    obj._slow_ema_values = data.SLOW_EMA_VALUES
    obj._hull_values = data.HULL_VALUES

    with patch.object(
        breakouts.util,
        "get_lookback_slices",
        return_value=data.BREAKOUT_SLICES,
    ) as mock_slices:
        result = obj.get_breakout_slices(candle_index=120)

    mock_slices.assert_called_once_with(
        candle_index=120,
        lookback=configs.fo_lookback,
        breakout_candles=data.CANDLES,
        fast_ema_values=data.FAST_EMA_VALUES,
        slow_ema_values=data.SLOW_EMA_VALUES,
        hull_values=data.HULL_VALUES,
    )

    assert result == data.BREAKOUT_SLICES


def test_get_valid_breakouts_returns_valid_breakouts(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = data.CANDLES
    obj.configs = configs
    obj.trend = "bullish"

    with (
        patch.object(
            obj,
            "get_breakout_slices",
            return_value=data.BREAKOUT_SLICES,
        ) as mock_slices,
        patch.object(
            breakouts.breakout,
            "BreakOut",
        ) as mock_breakout,
    ):
        mock_breakout.return_value.get_in_trend_breakout.return_value = (
            data.BREAKOUT_SIGNAL
        )

        result = obj.get_valid_breakouts()

    # 150 candles, starting at index 100 -> 50 iterations.
    assert len(result) == 50
    assert result == [data.BREAKOUT_SIGNAL] * 50

    assert mock_slices.call_count == 50
    assert mock_breakout.call_count == 50

    mock_breakout.assert_called_with(
        breakout_candles=data.BREAKOUT_SLICES["breakout_candles"],
        fast_ema_values=data.BREAKOUT_SLICES["fast_ema_values"],
        slow_ema_values=data.BREAKOUT_SLICES["slow_ema_values"],
        hull_values=data.BREAKOUT_SLICES["hull_values"],
        min_opposite_candles=configs.min_opposite_candles,
    )

    mock_breakout.return_value.get_in_trend_breakout.assert_called_with(
        min_score=configs.min_score,
        trend="bullish",
    )


def test_get_valid_breakouts_ignores_invalid_breakouts(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = data.CANDLES
    obj.configs = configs
    obj.trend = "bullish"

    with (
        patch.object(
            obj,
            "get_breakout_slices",
            return_value=data.BREAKOUT_SLICES,
        ),
        patch.object(
            breakouts.breakout,
            "BreakOut",
        ) as mock_breakout,
    ):
        mock_breakout.return_value.get_in_trend_breakout.return_value = None

        result = obj.get_valid_breakouts()

    assert result == []
    assert mock_breakout.call_count == 50


def test_get_valid_breakouts_returns_multiple_signals(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = data.CANDLES
    obj.configs = configs
    obj.trend = "bullish"

    with (
        patch.object(
            obj,
            "get_breakout_slices",
            return_value=data.BREAKOUT_SLICES,
        ),
        patch.object(
            breakouts.breakout,
            "BreakOut",
        ) as mock_breakout,
    ):
        mock_breakout.return_value.get_in_trend_breakout.side_effect = (
            [data.BREAKOUT_SIGNAL, None] * 25
        )

        result = obj.get_valid_breakouts()

    assert len(result) == 25
    assert all(
        signal == data.BREAKOUT_SIGNAL
        for signal in result
    )


def test_get_valid_breakouts_starts_at_candle_100(configs):
    candles = [
        data.candle(time=i)
        for i in range(105)
    ]

    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = candles
    obj.configs = configs
    obj.trend = "bullish"

    with (
        patch.object(
            obj,
            "get_breakout_slices",
            return_value=data.BREAKOUT_SLICES,
        ) as mock_slices,
        patch.object(
            breakouts.breakout,
            "BreakOut",
        ) as mock_breakout,
    ):
        mock_breakout.return_value.get_in_trend_breakout.return_value = None

        obj.get_valid_breakouts()

    assert mock_slices.call_count == 5

    assert (
        mock_slices.call_args_list[0].kwargs["candle_index"]
        == 100
    )

    assert (
        mock_slices.call_args_list[-1].kwargs["candle_index"]
        == 104
    )

    assert mock_breakout.call_count == 5


def test_get_valid_breakouts_returns_empty_for_less_than_101_candles(
    configs,
):
    candles = [
        data.candle(time=i)
        for i in range(100)
    ]

    obj = object.__new__(breakouts.Breakouts)

    obj._trading_tf_candles = candles
    obj.configs = configs
    obj.trend = "bullish"

    with patch.object(
        breakouts.breakout,
        "BreakOut",
    ) as mock_breakout:
        result = obj.get_valid_breakouts()

    assert result == []
    mock_breakout.assert_not_called()


def test_get_trade_signals_returns_none_when_no_breakouts(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj.configs = configs
    obj.interval = "30m"

    with patch.object(
        obj,
        "get_valid_breakouts",
        return_value=[],
    ):
        result = obj.get_trade_signals()

    assert result is None


def test_get_trade_signals_creates_trade_signals(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj.configs = configs
    obj.interval = "30m"

    breakout_signals = [
        data.BREAKOUT_SIGNAL,
        data.BREAKOUT_SIGNAL_2,
    ]

    with (
        patch.object(
            obj,
            "get_valid_breakouts",
            return_value=breakout_signals,
        ),
        patch.object(
            breakouts.util,
            "make_trade_signal",
            side_effect=[
                data.TRADE_SIGNAL,
                data.TRADE_SIGNAL_2,
            ],
        ) as mock_make_signal,
    ):
        result = obj.get_trade_signals()

    assert result == [
        data.TRADE_SIGNAL,
        data.TRADE_SIGNAL_2,
    ]

    assert mock_make_signal.call_count == 2

    mock_make_signal.assert_any_call(
        breakout_candle=data.BREAKOUT_SIGNAL["trigger_candle"],
        interval="30m",
        tp_rrrs=configs.tp_rrrs,
        sl_padding=configs.sl_padding,
        score=data.BREAKOUT_SIGNAL["score"],
    )

    mock_make_signal.assert_any_call(
        breakout_candle=data.BREAKOUT_SIGNAL_2["trigger_candle"],
        interval="30m",
        tp_rrrs=configs.tp_rrrs,
        sl_padding=configs.sl_padding,
        score=data.BREAKOUT_SIGNAL_2["score"],
    )


def test_get_trade_signals_uses_each_breakout(configs):
    obj = object.__new__(breakouts.Breakouts)

    obj.configs = configs
    obj.interval = "30m"

    breakout_signals = [
        data.BREAKOUT_SIGNAL,
        data.BREAKOUT_SIGNAL_2,
    ]

    with (
        patch.object(
            obj,
            "get_valid_breakouts",
            return_value=breakout_signals,
        ),
        patch.object(
            breakouts.util,
            "make_trade_signal",
            side_effect=[
                data.TRADE_SIGNAL,
                data.TRADE_SIGNAL_2,
            ],
        ) as mock_make_signal,
    ):
        obj.get_trade_signals()

    assert mock_make_signal.call_args_list == [
        call(
            breakout_candle=data.BREAKOUT_SIGNAL["trigger_candle"],
            interval="30m",
            tp_rrrs=configs.tp_rrrs,
            sl_padding=configs.sl_padding,
            score=data.BREAKOUT_SIGNAL["score"],
        ),
        call(
            breakout_candle=data.BREAKOUT_SIGNAL_2["trigger_candle"],
            interval="30m",
            tp_rrrs=configs.tp_rrrs,
            sl_padding=configs.sl_padding,
            score=data.BREAKOUT_SIGNAL_2["score"],
        ),
    ]


def test_get_latest_trade_signal_returns_none_when_no_trade_signals():
    obj = object.__new__(breakouts.Breakouts)

    with patch.object(
        obj,
        "get_trade_signals",
        return_value=None,
    ):
        result = obj.get_latest_trade_signal()

    assert result is None


def test_get_latest_trade_signal_returns_last_signal():
    obj = object.__new__(breakouts.Breakouts)

    trade_signals = [
        data.TRADE_SIGNAL,
        data.TRADE_SIGNAL_2,
    ]

    with patch.object(
        obj,
        "get_trade_signals",
        return_value=trade_signals,
    ):
        result = obj.get_latest_trade_signal()

    assert result == data.TRADE_SIGNAL_2



