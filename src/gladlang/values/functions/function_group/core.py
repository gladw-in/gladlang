"""Core FunctionGroup machinery: slots, construction, and repr."""

from gladlang.values.functions.base_function import BaseFunction


class FunctionGroupCore(BaseFunction):
    __slots__ = (
        "functions",
        "visibility",
        "is_static",
        "defining_class",
        "_call_count",
    )

    def __init__(self, name):
        super().__init__(name)
        self.functions = {}
        self.visibility = "PUBLIC"
        self.is_static = False
        self.defining_class = None
        self._call_count = 0

    def __repr__(self):
        return f"<function group {self.name}>"
