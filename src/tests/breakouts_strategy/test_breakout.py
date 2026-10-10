import pytest
from mooneazy.breakout_strategy.breakout_strategy import breakout
from . import breakout_data as data 


def test_resolve_level_with_dict():
    assert breakout.resolve_level({'value': 100}) == 100


@pytest.mark.parametrize('level', [100, 100.5])
def test_resolve_level_with_number(level):
    assert breakout.resolve_level(level) == level


def test_is_bullish():
    assert breakout.is_bullish(data.CANDLE_BULLISH)


def test_is_not_bullish():
    assert not breakout.is_bullish(data.CANDLE_BEARISH)


def test_equal_open_close_is_not_bullish():
    assert not breakout.is_bullish(data.CANDLE_DOJI)


def test_is_valid_min_oposit_bullish_breakout():
    assert breakout.is_valid_min_oposite(
        data.LOOKBACK_BEARISH,
        data.BULLISH_BREAKOUT,
        min_oposit=2,
    )


def test_is_valid_min_oposit_bearish_breakout():
    assert breakout.is_valid_min_oposite(
        data.LOOKBACK_BULLISH,
        data.BEARISH_BREAKOUT,
        min_oposit=2,
    )


def test_is_valid_min_oposit_returns_false_when_requirement_not_met():
    assert not breakout.is_valid_min_oposite(
        data.LOOKBACK_BULLISH,
        data.BULLISH_BREAKOUT,
        min_oposit=4,
    )


def test_is_valid_min_oposit_uses_one_third_by_default():
    assert breakout.is_valid_min_oposite(
        data.LOOKBACK_BEARISH,
        data.BULLISH_BREAKOUT,
    )


def test_is_bad_candle_bullish_close_too_far():
    candle = data.candle((100, 140, 95, 135))

    assert breakout.is_bad_candle(
        candle,
        range_high=110,
        range_low=90,
    )

def test_is_bad_candle_bullish_low_too_far():
    candle = data.candle((100, 110, 50, 105))

    assert breakout.is_bad_candle(
        candle,
        range_high=110,
        range_low=90,
    )


def test_is_bad_candle_bullish_inside_safe_zone():
    candle = data.candle((100, 110, 95, 108))

    assert not breakout.is_bad_candle(
        candle,
        range_high=110,
        range_low=90,
    )


def test_is_bad_candle_bearish_close_too_far():
    candle = data.candle((100, 105, 60, 65))

    assert breakout.is_bad_candle(
        candle,
        range_high=110,
        range_low=90,
    )
def test_is_bad_candle_bearish_high_too_far():
    candle = data.candle((100, 150, 95, 98))

    assert breakout.is_bad_candle(
        candle,
        range_high=110,
        range_low=90,
    )


def test_breaks_level_bullish():
    candle = data.candle((100, 110, 95, 108))

    assert breakout.breaks_level(candle, 100)


def test_breaks_level_bearish():
    candle = data.candle((100, 105, 90, 93))

    assert breakout.breaks_level(candle, 98)


def test_breaks_level_accepts_dict_level():
    assert breakout.breaks_level(
        data.CANDLE_BULLISH,
        {'value': 100},
    )


def test_breaks_level_returns_false_when_level_is_not_crossed():
    candle = data.candle((100, 105, 95, 102))

    assert not breakout.breaks_level(candle, 110)


def test_breaks_emas_when_both_are_broken():
    candle = data.candle((100, 110, 90, 108))

    assert breakout.breaks_emas(
        candle,
        fast_ema_value=100,
        slow_ema_value=102,
    )


def test_breaks_emas_returns_false_when_fast_not_broken():
    candle = data.candle((100, 110, 101, 108))

    assert not breakout.breaks_emas(
        candle,
        fast_ema_value=100,
        slow_ema_value=102,
    )


def test_touches():
    assert breakout.touches(
        data.TOUCHING_CANDLE,
        105,
    )


def test_touches_accepts_dict():
    assert breakout.touches(
        data.TOUCHING_CANDLE,
        {'value': 105},
    )


def test_touches_returns_false():
    assert not breakout.touches(
        data.NOT_TOUCHING_CANDLE,
        110,
    )


def test_count_indicator_touches():
    candles = [
        data.TOUCHING_CANDLE,
        data.NOT_TOUCHING_CANDLE,
        data.TOUCHING_CANDLE,
    ]

    values = [105, 110, 100]

    assert breakout.count_indicator_touches(
        candles,
        values,
    ) == 2


def test_count_indicator_touches_uses_last_candles():
    candles = [
        data.NOT_TOUCHING_CANDLE,
        data.TOUCHING_CANDLE,
        data.TOUCHING_CANDLE,
    ]

    values = [105, 100]

    assert breakout.count_indicator_touches(
        candles,
        values,
    ) == 2


@pytest.mark.parametrize(
    'no_of_touches,min_touches,expected',
    [
        (3, 3, True),
        (4, 3, True),
        (2, 3, False),
        (0, 1, False),
    ],
)
def test_is_tight_indicator(
    no_of_touches,
    min_touches,
    expected,
):
    assert breakout.is_tight_indicator(
        no_of_touches,
        min_touches,
    ) == expected


def test_is_cross_bullish():
    candle = data.candle((99, 110, 90, 108))

    assert breakout.is_cross(
        candle,
        data.FAST_EMAS_BULLISH_CROSS,
        data.SLOW_EMAS_BULLISH_CROSS,
    )


def test_is_cross_bearish():
    candle = data.candle((108, 110, 90, 95))

    assert breakout.is_cross(
        candle,
        data.FAST_EMAS_BEARISH_CROSS,
        data.SLOW_EMAS_BEARISH_CROSS,
    )


def test_is_cross_returns_false_without_ema_break():
    candle = data.candle((100, 105, 95, 102))

    fast = data.levels([100, 105])
    slow = data.levels([110, 108])

    assert not breakout.is_cross(
        candle,
        fast,
        slow,
    )


class TestBreakOut:

    def test_initializes_breakout_and_lookback_candles(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert (
            breakout_instance.breakout_candle
            == data.BREAKOUT_CANDLES[-1]
        )

        assert (
            breakout_instance.lookback_candles
            == data.BREAKOUT_CANDLES[:-1]
        )

        assert breakout_instance.min_opposit == 1

    def test_get_hull_touches(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        expected = breakout.count_indicator_touches(
            data.BREAKOUT_CANDLES,
            data.HULL_VALUES[
                -len(data.BREAKOUT_CANDLES):
            ],
        )

        assert breakout_instance.get_hull_touches() == expected

    def test_is_tight_hull(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._hull_touches = 3

        assert breakout_instance.is_tight_hull(
            min_touches=3,
        )

    def test_is_tight_hull_returns_false(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._hull_touches = 2

        assert not breakout_instance.is_tight_hull(
            min_touches=3,
        )

    def test_is_tight_fast_emas(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert breakout_instance.is_tight_fast_emas(
            min_touches=1,
        )

    def test_is_tight_slow_emas(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert breakout_instance.is_tight_slow_emas(
            min_touches=1,
        )

    def test_breaks_emas(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert breakout_instance.breaks_emas() == (
            breakout.breaks_emas(
                breakout_instance.breakout_candle,
                data.EMA_VALUES[-1],
                data.EMA_VALUES[-1],
            )
        )

    def test_is_engulfing(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert breakout_instance.is_engulfing() == (
            breakout.is_engulfing_breakout(
                data.BREAKOUT_CANDLES[:-1],
                data.BREAKOUT_CANDLES[-1],
                1,
            )
        )

    def test_get_score_returns_calculated_score(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        assert (
            breakout_instance.get_score()
            == breakout_instance._score
        )

    def test_is_valid_when_score_reaches_minimum(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._score = 8

        assert breakout_instance.is_valid(min_score=8)

    def test_is_invalid_when_score_is_below_minimum(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._score = 7

        assert not breakout_instance.is_valid(min_score=8)

    def test_get_in_trend_breakout_returns_signal_for_matching_trend(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._score = 8

        result = breakout_instance.get_in_trend_breakout(
            min_score=8,
            trend='buy',
        )

        assert result == {
            'trigger_candle': data.BREAKOUT_CANDLES[-1],
            'score': 8,
        }

    def test_get_in_trend_breakout_returns_none_for_wrong_trend(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._score = 8

        assert breakout_instance.get_in_trend_breakout(
            min_score=8,
            trend='sell',
        ) is None

    def test_get_in_trend_breakout_returns_none_when_score_is_too_low(self):
        breakout_instance = breakout.BreakOut(
            breakout_candles=data.BREAKOUT_CANDLES,
            fast_ema_values=data.EMA_VALUES,
            slow_ema_values=data.EMA_VALUES,
            hull_values=data.HULL_VALUES,
            min_opposite_candles=1,
        )

        breakout_instance._score = 7

        assert breakout_instance.get_in_trend_breakout(
            min_score=8,
            trend='buy',
        ) is None


