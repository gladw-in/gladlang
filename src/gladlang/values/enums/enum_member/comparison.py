"""Comparison for enum members."""

from gladlang.values.primitives.number import Number


class EnumMemberComparison:
    __slots__ = ()

    def get_comparison_eq(self, other, visited=None):
        from . import EnumMember

        if isinstance(other, EnumMember):
            equal = (
                self.enum_name == other.enum_name
                and self.member_name == other.member_name
            )

            return Number(int(equal)).set_context(self.context), None

        return Number(0).set_context(self.context), None

    def get_comparison_is(self, other):
        from . import EnumMember

        if isinstance(other, EnumMember):
            equal = (
                self.enum_name == other.enum_name
                and self.member_name == other.member_name
            )

            return Number(int(equal)).set_context(self.context), None

        return Number(0).set_context(self.context), None

    def get_comparison_ne(self, other):
        equal_result, error = self.get_comparison_eq(other)
        if error:
            return None, error

        return Number(1 - int(equal_result.is_true())).set_context(self.context), None
