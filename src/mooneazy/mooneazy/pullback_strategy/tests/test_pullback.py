
from pullback_strategy.pullback_strategy.pullback import get_pullback_details
import pytest
from pullback_strategy.tests import pivots_data


def test_get_pullback_details():
    min_fib = pivots_data.MIN_FIB
    max_fib = pivots_data.MAX_FIB
    assert get_pullback_details(
        pivots_data.pivots_case_1, min_fib, max_fib
    )['pullback_pivot'] == pivots_data.lookback_case_1

    assert get_pullback_details(
        pivots_data.pivots_case_2, min_fib, max_fib
    )['pullback_pivot'] == pivots_data.lookback_case_2

    assert get_pullback_details(
        pivots_data.pivots_case_3, min_fib, max_fib
    )['pullback_pivot'] == pivots_data.lookback_case_3




