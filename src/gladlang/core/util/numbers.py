"""Numeric validation helpers used by runtime operations."""

import math

from gladlang.core.errors import RuntimeError


def require_integer_number(
    value,
    position_start,
    position_end,
    context,
    name,
):
    if isinstance(value, int):
        return value, None

    if not math.isfinite(value):
        return None, RuntimeError(
            position_start,
            position_end,
            f"{name} must be finite",
            context,
        )

    if not float(value).is_integer():
        return None, RuntimeError(
            position_start,
            position_end,
            f"{name} must be an integer",
            context,
        )

    return int(value), None
