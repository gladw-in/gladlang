"""Interprets function body result in TCO trampoline, returning return or continue signal."""

from gladlang.core.errors import RuntimeError
from gladlang.values.nulls.tailcall import TailCall
from gladlang.values.primitives.number import Number


class BoundMethodHandleCallOutcome:
    __slots__ = ()

    def _handle_call_outcome(
        self,
        result,
        value_result,
        current_function,
        current_instance,
        new_context,
        interpreter,
        calling_context,
    ):
        from gladlang.values.functions.bound_method import BoundMethod

        if value_result.error:
            self._call_count = 0
            return ("return", value_result)

        if value_result.should_return:
            return_value = value_result.return_value

            if isinstance(return_value, TailCall):
                target_function = return_value.function
                if isinstance(target_function, BoundMethod):
                    return (
                        "continue",
                        target_function.function_to_bind,
                        target_function.instance,
                        return_value.arguments,
                    )
                else:
                    self._call_count = 0
                    return (
                        "return",
                        target_function.execute(
                            return_value.arguments, interpreter, calling_context
                        ),
                    )

            self._call_count = 0
            return ("return", result.success(return_value))

        if value_result.should_break or value_result.should_continue:
            self._call_count = 0
            return (
                "return",
                value_result.failure(
                    RuntimeError(
                        current_function.position_start,
                        current_function.position_end,
                        "Internal error: BREAK/CONTINUE escaped a function body",
                        new_context,
                    )
                ),
            )

        final_value = value_result.value or Number.null.copy()
        self._call_count = 0

        return ("return", result.success(final_value))
