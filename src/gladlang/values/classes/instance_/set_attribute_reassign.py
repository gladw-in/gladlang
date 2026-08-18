"""Attribute reassignment logic (including final checks and visibility)."""

from gladlang.core.errors import RuntimeError


class InstanceSetAttributeReassign:
    def _reassign_attribute(self, name_token, value, context, mangled_name):
        name = name_token.value

        if mangled_name and self.symbol_table.get(mangled_name):
            if mangled_name in self.symbol_table.finals:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot reassign constant '{name}'",
                    context,
                )

            update_error = self.symbol_table.update(mangled_name, value)
            if update_error:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    update_error,
                    context,
                )

            return value, None

        if self.symbol_table.get(name):
            current_visibility = self.symbol_table.get_visibility(name)
            defining_class = self.symbol_table.defining_classes.get(name)
            if defining_class is None:
                defining_class = self.class_reference

            access_error = self.check_access(
                name_token, current_visibility, defining_class, context
            )

            if access_error:
                return None, access_error

            if name in self.symbol_table.finals:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot reassign constant '{name}'",
                    context,
                )

            self.symbol_table.set(name, value, visibility=current_visibility)
            return value, None

        if self.class_reference.static_symbol_table.get(name):
            if name in self.class_reference.static_symbol_table.finals:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot shadow static constant '{name}' with an instance variable",
                    context,
                )

        set_error = self.symbol_table.set(
            name, value, visibility="PUBLIC", as_final=False
        )

        if set_error:
            return None, RuntimeError(
                name_token.position_start, name_token.position_end, set_error, context
            )

        return value, None
