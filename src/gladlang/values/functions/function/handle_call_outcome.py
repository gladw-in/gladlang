"""Interprets function body result and signals return, continue, or break for TCO loop."""

from gladlang.core.errors import RuntimeError
from gladlang.values.functions.bound_method import BoundMethod
from gladlang.values.nulls.tailcall import TailCall
from gladlang.values.primitives.number import Number


class FunctionHandleCallOutcome:
    __slots__ = ()

    def _handle_call_outcome(
        self, value_result, current_function, new_context, interpreter, calling_context
    ):
        if value_result.error:
            self._reset_call_counts(current_function)
            return ("return", value_result)

        if value_result.should_return:
            return_value = value_result.return_value
            if isinstance(return_value, TailCall):
                target_function = return_value.function
                if isinstance(target_function, BoundMethod):
                    self._call_count = 0

                    return (
                        "return",
                        target_function.execute(
                            return_value.arguments, interpreter, calling_context
                        ),
                    )
                else:
                    return ("continue", target_function, return_value.arguments)

            return ("break", return_value)

        if value_result.should_break or value_result.should_continue:
            self._reset_call_counts(current_function)
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

        return ("break", value_result.value or Number.null.copy())
