"""Attribute setting: declaration of new attributes (with visibility/final)."""

from gladlang.core.errors import RuntimeError


class InstanceSetAttribute:
    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        name = name_token.value

        if visibility == "FINAL":
            visibility = "PUBLIC"
            as_final = True

        mangled_name = None
        if context and context.active_class:
            mangled_name = f"_{context.active_class.name}__{name}"

        if visibility is not None or as_final:
            target_name = mangled_name if visibility == "PRIVATE" else name
            if target_name in self.symbol_table.symbols:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Attribute '{name}' is already defined",
                    context,
                )

            self.symbol_table.set(
                target_name,
                value,
                visibility=(visibility or "PUBLIC"),
                as_final=as_final,
                defining_class=context.active_class if context else None,
            )

            if visibility == "PRIVATE" and self.symbol_table.get(name):
                if name in self.symbol_table.finals:
                    return None, RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        f"Cannot shadow constant '{name}' with a private variable",
                        context,
                    )
                self.symbol_table.remove(name)

            return value, None

        return self._reassign_attribute(name_token, value, context, mangled_name)
