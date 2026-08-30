"""String `+` (concatenation with String or Number) and `*` (repetition)."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.values.primitives.number import Number


class StringArithmetic:
    __slots__ = ()

    def added_to(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, String):
            new_length = len(self.value) + len(other.value)
            if new_length > Settings.MAX_STRING_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"String concatenation result ({new_length:,} chars) exceeds maximum allowed size ({Settings.MAX_STRING_SIZE:,} chars)",
                    self.context,
                )

            return String(self.value + other.value).set_context(self.context), None

        elif isinstance(other, Number):
            suffix = str(other.value)
            new_length = len(self.value) + len(suffix)
            if new_length > Settings.MAX_STRING_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"String concatenation result exceeds maximum allowed size ({Settings.MAX_STRING_SIZE:,} chars)",
                    self.context,
                )

            return String(self.value + suffix).set_context(self.context), None

        return None, self._illegal(other)

    def multed_by(self, other):
        from gladlang.values.primitives.string import String

        if isinstance(other, Number):
            multiplier_raw = other.value
            if isinstance(multiplier_raw, float) and not multiplier_raw.is_integer():
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"String repetition count must be a whole number, got {multiplier_raw}",
                    self.context,
                )

            multiplier = int(multiplier_raw)
            if multiplier < 0:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "String repetition count cannot be negative",
                    self.context,
                )

            new_length = len(self.value) * multiplier
            if new_length > Settings.MAX_STRING_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"String repetition result ({new_length:,} chars) exceeds maximum allowed size ({Settings.MAX_STRING_SIZE:,} chars)",
                    self.context,
                )

            return String(self.value * multiplier).set_context(self.context), None

        return None, self._illegal(other)
