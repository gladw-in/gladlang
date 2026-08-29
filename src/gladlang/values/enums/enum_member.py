"""EnumMember – a wrapper that represents a single enum case."""

from gladlang.values.primitives.number import Number
from gladlang.values.value import Value


class EnumMember(Value):
    __slots__ = (
        "enum_name",
        "member_name",
        "value",
        "position_start",
        "position_end",
        "context",
    )

    def __init__(self, enum_name, member_name, value):
        self.enum_name = enum_name
        self.member_name = member_name
        self.value = value
        self.position_start = self.position_end = self.context = None

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def get_attribute(self, name_token, context=None):
        if name_token.value == "value":
            return self.value, None

        return None, self.illegal_operation()

    def get_comparison_eq(self, other, visited=None):
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

    def get_comparison_is(self, other):
        if isinstance(other, EnumMember):
            equal = (
                self.enum_name == other.enum_name
                and self.member_name == other.member_name
            )

            return Number(int(equal)).set_context(self.context), None

        return Number(0).set_context(self.context), None

    def get_comparison_instanceof(self, other):
        from gladlang.values.classes.type_ import Type
        from gladlang.values.classes.class_ import Class

        if isinstance(other, Type):
            if other.name in ("Enum", "Object"):
                return Number.true.copy(), None

            return Number.false.copy(), None

        if isinstance(other, Class):
            return Number.false.copy(), None

        from gladlang.core.errors import RuntimeError

        return None, RuntimeError(
            self.position_start,
            self.position_end,
            "Right operand of INSTANCEOF must be a Class or Type",
            self.context,
        )

    def copy(self):
        member_copy = EnumMember(self.enum_name, self.member_name, self.value)

        return member_copy.set_position(
            self.position_start, self.position_end
        ).set_context(self.context)

    def __repr__(self):
        return f"{self.enum_name}.{self.member_name}"
