"""Number comparisons: IS, ==, !=, <, >, <=, >=."""


class NumberComparisons:
    __slots__ = ()

    def get_comparison_is(self, other):
        from gladlang.values.primitives.number import Number

        return Number(1 if self is other else 0).set_context(self.context), None

    def get_comparison_eq(self, other, visited=None):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null"):
            return Number(0).set_context(self.context), None

        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_ne(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null"):
            return Number(1).set_context(self.context), None

        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_lt(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_gt(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

        return None, self._illegal(other)

    def get_comparison_lte(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)

    def get_comparison_gte(self, other):
        from gladlang.values.primitives.number import Number

        if hasattr(other, "_is_null") and other._is_null:
            return None, self._illegal(other)

        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )

        return None, self._illegal(other)
