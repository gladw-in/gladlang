"""List `+` (concatenation) and `*` (repetition), both with size-limit checks."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.values.primitives.number import Number


class ListArithmetic:
    __slots__ = ()

    def added_to(self, other):
        from gladlang.values.primitives.list import List

        if isinstance(other, List):
            new_length = len(self.elements) + len(other.elements)
            if new_length > Settings.MAX_LIST_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"List concatenation result ({new_length}) exceeds maximum allowed size ({Settings.MAX_LIST_SIZE})",
                    self.context,
                )

            new_list = List(self.elements + other.elements)
            new_list.set_context(self.context)

            return new_list, None

        return None, self._illegal(other)

    def multed_by(self, other):
        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        from gladlang.values.primitives.list import List

        if isinstance(other, Number):
            multiplier_raw = other.value
            if isinstance(multiplier_raw, float) and not multiplier_raw.is_integer():
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"List repetition count must be a whole number, got {multiplier_raw}",
                    self.context,
                )

            multiplier = int(multiplier_raw)
            if multiplier < 0:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    "List repetition count cannot be negative",
                    self.context,
                )

            result_length = len(self.elements) * multiplier
            if result_length > Settings.MAX_LIST_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"List repetition result ({result_length}) exceeds maximum allowed size ({Settings.MAX_LIST_SIZE})",
                    self.context,
                )

            new_list = List(self.elements * multiplier)
            new_list.set_context(self.context)

            return new_list, None
        return None, self._illegal(other)
