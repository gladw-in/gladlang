"""BaseFunction's INSTANCEOF comparison against Type/Class values."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class BaseFunctionInstanceof:
    __slots__ = ()

    def get_comparison_instanceof(self, other):
        from gladlang.values.classes.type_ import Type
        from gladlang.values.classes.class_ import Class

        if isinstance(other, Type):
            if other.name == "Function":
                return Number.true.copy(), None

            if other.name == "Object":
                return Number.true.copy(), None

            return Number.false.copy(), None

        if isinstance(other, Class):
            return Number.false.copy(), None

        return None, RuntimeError(
            self.position_start,
            self.position_end,
            "Right operand of INSTANCEOF must be a Class or Type",
            self.context,
        )
