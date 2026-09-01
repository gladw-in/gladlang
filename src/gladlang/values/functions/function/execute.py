"""Trampoline loop for function execution with TCO."""

from gladlang.runtime.runtime_result import RuntimeResult


class FunctionExecute:
    __slots__ = ()

    def execute(self, arguments, interpreter, calling_context=None):
        result = RuntimeResult()

        current_function = self
        current_arguments = arguments
        base_depth = None
        final_result = None

        while True:
            current_function, error_result = self._resolve_overload(
                current_function, current_arguments
            )

            if error_result is not None:
                return error_result

            if not hasattr(current_function, "body_node"):
                return current_function.execute(
                    current_arguments, interpreter, calling_context
                )

            new_context, base_depth, error_result = self._setup_call_context(
                current_function, calling_context, base_depth
            )

            if error_result is not None:
                return error_result

            result.register(
                current_function.check_and_populate_arguments(
                    getattr(current_function, "argument_names", None),
                    current_arguments,
                    new_context,
                )
            )

            if result.error:
                self._reset_call_counts(current_function)
                return result

            value_result = interpreter.visit(current_function.body_node, new_context)

            outcome = self._handle_call_outcome(
                value_result,
                current_function,
                new_context,
                interpreter,
                calling_context,
            )

            if outcome[0] == "return":
                return outcome[1]
            elif outcome[0] == "continue":
                _, current_function, current_arguments = outcome
                result = RuntimeResult()
                continue
            else:
                final_result = outcome[1]
                break

        self._reset_call_counts(current_function)
        return result.success(final_result)

    def _reset_call_counts(self, current_function):
        self._call_count = 0
        if current_function is not self:
            current_function._call_count = 0
