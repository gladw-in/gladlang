"""Set static attribute on class with declaration, reassignment, and constant checks."""

from gladlang.core.errors import RuntimeError


class ClassSetAttribute:
    __slots__ = ()

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        name = name_token.value
        if visibility == "FINAL":
            visibility = "PUBLIC"
            as_final = True

        is_declaration = visibility is not None or as_final

        defining_class = None
        for current_class in self.mro:
            if current_class.static_symbol_table.get(name) is not None:
                defining_class = current_class
                break

        if is_declaration:
            if (
                defining_class is not None
                and defining_class is not self
                and name in defining_class.static_symbol_table.finals
            ):
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot shadow static constant '{name}' declared in '{defining_class.name}'",
                    context,
                )

            self.static_symbol_table.set(
                name,
                value,
                visibility=(visibility or "PUBLIC"),
                as_final=as_final,
                defining_class=self,
            )
            self._method_cache.clear()
            return value, None

        target_class = defining_class if defining_class is not None else self

        if name in target_class.static_symbol_table.finals:
            return None, RuntimeError(
                name_token.position_start,
                name_token.position_end,
                f"Cannot reassign static constant '{name}'",
                context,
            )

        if defining_class is not None:
            error = target_class.static_symbol_table.update(name, value)
        else:
            error = target_class.static_symbol_table.set(
                name,
                value,
                visibility=(visibility or "PUBLIC"),
                as_final=as_final,
                defining_class=self,
            )

        if error:
            return None, RuntimeError(
                name_token.position_start, name_token.position_end, error, context
            )

        target_class._method_cache.clear()

        return value, None
