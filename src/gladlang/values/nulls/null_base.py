"""NullBase – base class for null and boolean singletons, providing comparison logic"""

from gladlang.values.primitives.number import Number


class NullBase(Number):
    __slots__ = ("_is_null",)

    def __init__(self, value, is_null=False):
        super().__init__(value)
        self._is_null = is_null

    def get_comparison_eq(self, other, visited=None):
        if hasattr(other, "class_reference") and hasattr(other, "symbol_table"):
            if self._is_null:
                return Number(0).set_context(self.context), None

        if isinstance(other, (NullBase)):
            are_equal = self._is_null == other._is_null and self.value == other.value
            return Number(int(are_equal)).set_context(self.context), None

        return Number(0).set_context(self.context), None

    def get_comparison_ne(self, other):
        equal_result, error = self.get_comparison_eq(other)
        if error:
            return None, error

        return Number(1 - int(equal_result.is_true())).set_context(self.context), None

    def get_comparison_lt(self, other):
        if self._is_null:
            return None, self._illegal(other)

        return super().get_comparison_lt(other)

    def get_comparison_gt(self, other):
        if self._is_null:
            return None, self._illegal(other)

        return super().get_comparison_gt(other)

    def get_comparison_lte(self, other):
        if self._is_null:
            return None, self._illegal(other)

        return super().get_comparison_lte(other)

    def get_comparison_gte(self, other):
        if self._is_null:
            return None, self._illegal(other)

        return super().get_comparison_gte(other)

    def _illegal(self, other=None):
        if not other:
            other = self

        from gladlang.core.errors import RuntimeError

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def is_true(self):
        if self._is_null:
            return False

        return bool(self.value)

    def __repr__(self):
        if self._is_null:
            return "null"

        return str(self.value)
