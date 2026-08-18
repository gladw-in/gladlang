"""Built-in: LEN (length of a String, List, or Dict)."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.bound_method import BoundMethod
from gladlang.values.functions.function import Function
from gladlang.values.functions.function_group import FunctionGroup
from gladlang.values.primitives.dict import Dict
from gladlang.values.primitives.list import List
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class BuiltInFunctionLen:
    __slots__ = ()

    def _execute_len(self, arguments, call_context, calling_context):
        result = RuntimeResult()
        result.register(
            self.check_arguments(["value"], arguments, calling_context=calling_context)
        )
        if result.error:
            return result

        argument = arguments[0]
        if isinstance(argument, String):
            return result.success(Number(len(argument.value)))
        elif isinstance(argument, List):
            return result.success(Number(len(argument.elements)))
        elif isinstance(argument, Dict):
            return result.success(Number(len(argument.elements)))
        elif isinstance(argument, Number):
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "LEN is not defined for Number, use STR(n) first if you want the digit count",
                    call_context,
                )
            )
        else:
            from gladlang.values.classes.class_ import Class
            from gladlang.values.functions.built_in_function import BuiltInFunction

            if isinstance(
                argument, (Function, FunctionGroup, BoundMethod, BuiltInFunction, Class)
            ):
                return result.failure(
                    RuntimeError(
                        self.position_start,
                        self.position_end,
                        f"LEN is not defined for type '{type(argument).__name__}'",
                        call_context,
                    )
                )

            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    f"LEN is not supported for type '{type(argument).__name__}'",
                    call_context,
                )
            )
