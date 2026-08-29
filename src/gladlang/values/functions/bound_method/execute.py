"""Trampoline loop for bound method calls with TCO."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.function_group import FunctionGroup


class BoundMethodExecute:
    __slots__ = ()

    def execute(self, arguments, interpreter, calling_context=None):
        result = RuntimeResult()

        if isinstance(self.function_to_bind, FunctionGroup):
            return self._execute_function_group_directly(
                arguments, interpreter, calling_context
            )

        current_function = self.function_to_bind
        current_instance = self.instance
        current_arguments = arguments
        base_depth = None

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
                    [current_instance] + current_arguments,
                    new_context,
                )
            )

            if result.error:
                self._call_count = 0
                return result

            value_result = interpreter.visit(current_function.body_node, new_context)

            outcome = self._handle_call_outcome(
                result,
                value_result,
                current_function,
                current_instance,
                new_context,
                interpreter,
                calling_context,
            )

            if outcome[0] == "return":
                return outcome[1]
            else:
                _, current_function, current_instance, current_arguments = outcome
                result = RuntimeResult()
                continue

    def _execute_function_group_directly(self, arguments, interpreter, calling_context):
        full_arguments = [self.instance] + arguments
        function_group = self.function_to_bind

        if function_group.context is None or function_group.position_start is None:
            function_group = function_group.copy()
            if self.context is not None:
                function_group.set_context(self.context)

            function_group.set_position(self.position_start, self.position_end)

        return function_group.execute(full_arguments, interpreter, calling_context)
