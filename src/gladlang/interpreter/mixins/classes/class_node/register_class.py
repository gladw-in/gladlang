"""Store the finished methods on the class and save the class in the symbol table."""

from gladlang.values.classes.class_ import Class


class InterpreterClassNodeRegisterClass:
    def _register_class(self, context, class_name, class_value, methods):
        class_value.methods = methods
        class_value._method_cache.clear()

        existing = context.symbol_table.get(class_name)
        if existing is not None and isinstance(existing, Class):
            context.symbol_table.remove(class_name)

        context.symbol_table.set(class_name, class_value)
