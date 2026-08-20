"""Helper for binding FOR-loop variables, including list-destructuring targets."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.list import List


class InterpreterLoopUnpack:
    def unpack_and_set(self, variable_tokens, element_value, context, result):
        if len(variable_tokens) == 1:
            variable_name = variable_tokens[0].value
            current_table = context.symbol_table
            while current_table:
                if variable_name in current_table.finals:
                    return result.failure(
                        RuntimeError(
                            variable_tokens[0].position_start,
                            variable_tokens[0].position_end,
                            f"Cannot use constant '{variable_name}' as loop variable",
                            context,
                        )
                    )

                current_table = current_table.parent

            context.symbol_table.set(variable_name, element_value)

            return True

        if not isinstance(element_value, List):
            return result.failure(
                RuntimeError(
                    variable_tokens[0].position_start,
                    variable_tokens[-1].position_end,
                    f"Cannot unpack type '{type(element_value).__name__}' (expected List)",
                    context,
                )
            )

        if len(element_value.elements) != len(variable_tokens):
            return result.failure(
                RuntimeError(
                    variable_tokens[0].position_start,
                    variable_tokens[-1].position_end,
                    f"Cannot unpack {len(element_value.elements)} value(s) into {len(variable_tokens)} variable(s)",
                    context,
                )
            )

        for index, token in enumerate(variable_tokens):
            variable_name = token.value
            current_table = context.symbol_table
            while current_table:
                if variable_name in current_table.finals:
                    return result.failure(
                        RuntimeError(
                            token.position_start,
                            token.position_end,
                            f"Cannot use constant '{variable_name}' as loop variable",
                            context,
                        )
                    )

                current_table = current_table.parent

            context.symbol_table.set(variable_name, element_value.elements[index])

        return True
