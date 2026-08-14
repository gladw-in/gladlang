"""Attribute lookup: instance own symbol table + mangled private access."""

from gladlang.core.errors import RuntimeError


class InstanceGetAttribute:
    def get_attribute(self, name_token, context=None):
        name = name_token.value

        if context and context.active_class:
            mangled_self = f"_{context.active_class.name}__{name}"
            mangled_value = self.symbol_table.get(mangled_self)
            if mangled_value is not None:
                return mangled_value, None

        if self.class_reference:
            current_class = context.active_class if context else None
            if current_class:
                mangled_current = f"_{current_class.name}__{name}"
                mangled_value = self.symbol_table.get(mangled_current)
                if mangled_value is not None:
                    return mangled_value, None

            for mro_class in self.class_reference.mro:
                mangled_name = f"_{mro_class.name}__{name}"
                mangled_value = self.symbol_table.get(mangled_name)
                if mangled_value is not None:
                    if context and context.active_class == mro_class:
                        return mangled_value, None
                    else:
                        return None, RuntimeError(
                            name_token.position_start,
                            name_token.position_end,
                            f"Cannot access private member '{name}'",
                            context,
                        )

        value = self.symbol_table.get(name)
        if value is not None:
            visibility = self.symbol_table.get_visibility(name)
            if visibility != "PUBLIC":
                defining_class = self.symbol_table.defining_classes.get(name)
                if defining_class is None:
                    defining_class = self.class_reference
            else:
                defining_class = self.class_reference

            access_error = self.check_access(
                name_token, visibility, defining_class, context
            )

            if access_error:
                return None, access_error

            return value, None

        return self._get_attribute_class_member(name_token, context)
