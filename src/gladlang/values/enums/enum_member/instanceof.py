"""Instanceof comparison for enum members."""

from gladlang.values.primitives.number import Number


class EnumMemberInstanceof:
    __slots__ = ()

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
