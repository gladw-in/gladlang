"""Create the Class value for a CLASS declaration and compute its MRO."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.classes.class_ import Class


class InterpreterClassNodeCreateClass:
    def _create_class_value(
        self, result, class_node, context, class_name, superclasses
    ):
        static_table = SymbolTable(parent=context.symbol_table)
        class_value = Class(class_name, superclasses, {}, static_table)
        class_value.set_context(context).set_position(
            class_node.position_start, class_node.position_end
        )

        mro, error = self.compute_mro(class_value)
        if error:
            return (
                None,
                None,
                result.failure(
                    RuntimeError(
                        class_node.position_start,
                        class_node.position_end,
                        error,
                        context,
                    )
                ),
            )

        class_value.mro = mro

        return class_value, static_table, None
