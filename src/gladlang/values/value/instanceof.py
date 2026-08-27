"""Check if a value is an instance of a built-in type."""

from gladlang.core.errors import RuntimeError


class ValueInstanceof:
    __slots__ = ()

    def get_comparison_instanceof(self, other):
        from gladlang.values.primitives.number import Number
        from gladlang.values.classes.type_ import Type
        from gladlang.values.classes.class_ import Class
        from gladlang.values.primitives.number import Number as Num
        from gladlang.values.primitives.string import String
        from gladlang.values.primitives.list import List
        from gladlang.values.primitives.dict import Dict
        from gladlang.values.functions.base_function import BaseFunction

        if isinstance(other, Type):
            if other.name == "Number" and isinstance(self, Num):
                return Number.true.copy(), None

            if other.name == "String" and isinstance(self, String):
                return Number.true.copy(), None

            if other.name == "List" and isinstance(self, List):
                return Number.true.copy(), None

            if other.name == "Dict" and isinstance(self, Dict):
                return Number.true.copy(), None

            if other.name == "Function" and isinstance(self, BaseFunction):
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
