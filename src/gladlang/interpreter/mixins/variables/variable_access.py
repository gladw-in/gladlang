"""Visitor for variable reads, including the special THIS/SUPER identifiers."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.classes.instance_ import Instance
from gladlang.values.classes.super_ import Super


class InterpreterVariableAccess:
    def visit_VariableAccessNode(self, node, context):
        result = RuntimeResult()

        if context is None:
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    "Internal error: missing execution context",
                    None,
                )
            )

        variable_name = node.variable_name_token.value

        if variable_name == "SUPER":
            instance = context.symbol_table.get("THIS")
            if not instance or not isinstance(instance, Instance):
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        "'SUPER' can only be used inside an instance method",
                        context,
                    )
                )

            current_class = context.active_class
            if not current_class:
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        "'SUPER' cannot be used outside of a class context",
                        context,
                    )
                )

            super_value = (
                Super(instance, current_class)
                .set_context(context)
                .set_position(node.position_start, node.position_end)
            )

            return result.success(super_value)

        if variable_name == "THIS" and context.is_static:
            local_this = context.symbol_table.get("THIS")
            if local_this is None:
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        "'THIS' cannot be used inside a static method",
                        context,
                    )
                )

        value = context.symbol_table.get(variable_name)
        if value is None:
            return result.failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    f"'{variable_name}' is not defined",
                    context,
                )
            )

        return result.success(value)
