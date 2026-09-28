"""Deterministic calculation helpers for economic indicator analysis."""

from __future__ import annotations

import math

Number = int | float
ZERO_BASELINE_ABS_TOLERANCE = 1e-12


def _validate_numeric(value: Number, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        msg = f"{name} must be a real number"
        raise TypeError(msg)

    numeric_value = float(value)
    if not math.isfinite(numeric_value):
        msg = f"{name} must be finite"
        raise ValueError(msg)

    return numeric_value


def absolute_change(previous: Number, current: Number) -> float:
    """Return the absolute difference between the current and previous values."""

    previous_value = _validate_numeric(previous, name="previous")
    current_value = _validate_numeric(current, name="current")
    return current_value - previous_value


def percentage_change(previous: Number, current: Number) -> float:
    """Return percent change, raising when the baseline is zero or effectively zero."""

    previous_value = _validate_numeric(previous, name="previous")
    current_value = _validate_numeric(current, name="current")
    if math.isclose(
        previous_value, 0.0, rel_tol=0.0, abs_tol=ZERO_BASELINE_ABS_TOLERANCE
    ):
        msg = "percentage change is undefined for a zero baseline"
        raise ValueError(msg)

    return ((current_value - previous_value) / previous_value) * 100.0


def percentage_point_change(previous: Number, current: Number) -> float:
    """Return the arithmetic difference for rate or share comparisons."""

    previous_value = _validate_numeric(previous, name="previous")
    current_value = _validate_numeric(current, name="current")
    return current_value - previous_value
