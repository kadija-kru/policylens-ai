import math

import pytest
from policylens.tools.calculations import (
    absolute_change,
    percentage_change,
    percentage_point_change,
)


def test_absolute_change_positive() -> None:
    assert absolute_change(100, 125) == pytest.approx(25.0)


def test_absolute_change_negative() -> None:
    assert absolute_change(125, 100) == pytest.approx(-25.0)


def test_percentage_change_positive() -> None:
    assert percentage_change(100, 125) == pytest.approx(25.0)


def test_percentage_change_negative_baseline_value() -> None:
    assert percentage_change(-100, -80) == pytest.approx(-20.0)


def test_percentage_change_zero_baseline_is_explicitly_undefined() -> None:
    with pytest.raises(ValueError, match="zero baseline"):
        percentage_change(0, 10)


def test_percentage_change_negative_zero_baseline_is_explicitly_undefined() -> None:
    with pytest.raises(ValueError, match="zero baseline"):
        percentage_change(-0.0, 10)


def test_percentage_point_change_for_rates() -> None:
    assert percentage_point_change(6.3, 6.5) == pytest.approx(0.2)


def test_invalid_inputs_raise_for_non_numeric_values() -> None:
    with pytest.raises(TypeError, match="previous must be a real number"):
        absolute_change("100", 110)  # type: ignore[arg-type]


def test_invalid_inputs_raise_for_non_finite_values() -> None:
    with pytest.raises(ValueError, match="current must be finite"):
        percentage_point_change(1.0, math.inf)
