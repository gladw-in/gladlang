"""Visitor for enum definitions."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.enums.enum import Enum
from gladlang.values.primitives.number import Number


class InterpreterEnums:
    def visit_EnumNode(self, node, context):
        result = RuntimeResult()

        enum_name = node.enum_name_token.value
        elements_dictionary = {}
        current_value = 0

        for case_name_token, case_value_node in node.cases:
            case_name = case_name_token.value
            if case_name in elements_dictionary:
                return result.failure(
                    RuntimeError(
                        case_name_token.position_start,
                        case_name_token.position_end,
                        f"Duplicate enum case '{case_name}'",
                        context,
                    )
                )

            if case_value_node:
                case_value = result.register(self.visit(case_value_node, context))
                if result.error:
                    return result

                if isinstance(case_value, Number):
                    current_value = int(case_value.value)

            else:
                case_value = Number(current_value).set_context(context)

            elements_dictionary[case_name] = case_value
            if isinstance(case_value, Number):
                current_value += 1

        enum_value = Enum(enum_name, elements_dictionary)
        enum_value.set_context(context).set_position(
            node.position_start, node.position_end
        )

        visibility_level = getattr(node, "visibility", "PUBLIC")

        defining_class = context.active_class if context.active_class else None

        context.symbol_table.set(
            enum_name,
            enum_value,
            visibility=visibility_level,
            as_final=True,
            defining_class=defining_class,
        )

        return result.success(enum_value)
