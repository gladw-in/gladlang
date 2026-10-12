"""Add a method to the methods dict, turning same-name methods into an overload group."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.function_group import FunctionGroup


class InterpreterBuildMethodsAddOverload:
    def _add_method_overload(self, methods, method_name, method_value):
        if method_name in methods:
            existing = methods[method_name]
            if isinstance(existing, FunctionGroup):
                add_error = existing.add_function(method_value)
                if (
                    add_error
                    and isinstance(add_error, RuntimeResult)
                    and add_error.error
                ):
                    return add_error

            else:
                group = FunctionGroup(method_name)
                group.add_function(existing)
                add_error = group.add_function(method_value)
                if (
                    add_error
                    and isinstance(add_error, RuntimeResult)
                    and add_error.error
                ):
                    return add_error

                methods[method_name] = group
        else:
            methods[method_name] = method_value

        return None
