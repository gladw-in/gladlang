"""Bitwise NOT (~) for numbers."""

from gladlang.core.util.numbers import require_integer_number
from gladlang.core.util.settings import Settings


class NumberBitwiseNot:
    __slots__ = ()

    def bitted_not(self):
        from gladlang.values.primitives.number import Number

        operand, error = require_integer_number(
            self.value,
            self.position_start,
            self.position_end,
            self.context,
            "Operand",
        )

        if error:
            return None, error

        raw_value = (~operand) & Settings.BITWISE_MASK
        if raw_value & Settings.BITWISE_SIGN_BIT:
            raw_value -= Settings.BITWISE_COMPLEMENT

        return Number(raw_value).set_context(self.context), None
