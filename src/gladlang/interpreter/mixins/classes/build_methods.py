"""Build class methods from method nodes, grouping overloads and enforcing LSP."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.functions.function import Function
from gladlang.values.functions.function_group import FunctionGroup


class InterpreterBuildMethods:
    def _build_methods(self, result, node, context, class_value):
        methods = {}
        for method_node in node.method_nodes:
            method_name = method_node.variable_name_token.value
            method_value = Function(
                method_name,
                method_node.body_node,
                method_node.argument_name_tokens,
                context,
                getattr(method_node, "visibility", "PUBLIC"),
                class_value,
                getattr(method_node, "is_static", False),
            ).set_position(method_node.position_start, method_node.position_end)

            if method_name in methods:
                existing = methods[method_name]
                if isinstance(existing, FunctionGroup):
                    add_error = existing.add_function(method_value)
                    if (
                        add_error
                        and isinstance(add_error, RuntimeResult)
                        and add_error.error
                    ):
                        return None, add_error

                else:
                    group = FunctionGroup(method_name)
                    group.add_function(existing)
                    add_error = group.add_function(method_value)
                    if (
                        add_error
                        and isinstance(add_error, RuntimeResult)
                        and add_error.error
                    ):
                        return None, add_error

                    methods[method_name] = group
            else:
                methods[method_name] = method_value

            parent_method = None
            for ancestor in class_value.mro:
                if ancestor == class_value:
                    continue

                if method_name in ancestor.methods:
                    parent_method = ancestor.methods[method_name]
                    break

            if parent_method:
                visibility_levels = {"PUBLIC": 3, "PROTECTED": 2, "PRIVATE": 1}
                parent_visibility_score = visibility_levels.get(
                    parent_method.visibility, 3
                )
                child_visibility_score = visibility_levels.get(
                    method_value.visibility, 3
                )

                if child_visibility_score < parent_visibility_score:
                    return None, result.failure(
                        RuntimeError(
                            method_node.position_start,
                            method_node.position_end,
                            f"Method '{method_name}' cannot be more restrictive than parent method (LSP Violation)",
                            context,
                        )
                    )

        return methods, None
