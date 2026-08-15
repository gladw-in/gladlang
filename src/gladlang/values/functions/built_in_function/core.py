"""Core BuiltInFunction machinery: construction, copy, repr."""

from gladlang.values.functions.base_function import BaseFunction


class BuiltInFunctionCore(BaseFunction):
    __slots__ = ()

    def __init__(self, name):
        super().__init__(name)

    def copy(self):
        from gladlang.values.functions.built_in_function import BuiltInFunction

        function_copy = BuiltInFunction(self.name)
        function_copy.set_context(self.context)
        function_copy.set_position(self.position_start, self.position_end)
        return function_copy

    def __repr__(self):
        return f"<built-in function {self.name}>"
