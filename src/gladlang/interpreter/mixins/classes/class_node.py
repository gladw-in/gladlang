"""Visitor for CLASS declarations: builds the Class value, computes its MRO, evaluates static fields, and builds its methods."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.context import Context
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.classes.class_ import Class


class InterpreterClassNode:
    def visit_ClassNode(self, class_node, context):
        result = RuntimeResult()

        class_name = class_node.class_name_token.value

        superclasses = self._resolve_superclasses(
            result, class_node, context, class_name
        )

        if result.error:
            return result

        for superclass in superclasses:
            if len(superclass.mro) >= Settings.MAX_INHERITANCE_DEPTH:
                return result.failure(
                    RuntimeError(
                        class_node.position_start,
                        class_node.position_end,
                        f"Inheritance chain too deep (exceeds limit of {Settings.MAX_INHERITANCE_DEPTH})",
                        context,
                    )
                )

        static_table = SymbolTable(parent=context.symbol_table)
        class_value = Class(class_name, superclasses, {}, static_table)
        class_value.set_context(context).set_position(
            class_node.position_start, class_node.position_end
        )

        mro, error = self.compute_mro(class_value)
        if error:
            return result.failure(
                RuntimeError(
                    class_node.position_start, class_node.position_end, error, context
                )
            )

        class_value.mro = mro

        class_context = Context(
            f"<class {class_name}>", context, class_node.position_start
        )
        class_context.symbol_table = static_table
        class_context.active_class = class_value

        for field_node in class_node.static_field_nodes:
            result.register(self.visit(field_node, class_context))
            if result.error:
                return result

        static_table.parent = None

        methods, build_error = self._build_methods(
            result, class_node, context, class_value
        )

        if build_error is not None:
            return build_error

        class_value.methods = methods
        class_value._method_cache.clear()

        existing = context.symbol_table.get(class_name)
        if existing is not None and isinstance(existing, Class):
            context.symbol_table.remove(class_name)

        context.symbol_table.set(class_name, class_value)

        return result.success(class_value)
