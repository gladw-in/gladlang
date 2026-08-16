"""Try to get a static field from an MRO class with visibility checks."""

from gladlang.core.errors import RuntimeError


class ClassGetAttributeStaticField:
    __slots__ = ()

    def _try_static_field(
        self, current_class, method_name, name_token, context, cache_key
    ):
        value = current_class.static_symbol_table.get(method_name)
        if value is None:
            return None

        visibility = current_class.static_symbol_table.get_visibility(method_name)
        defining_class = current_class
        if visibility == "PRIVATE" and (
            not context or context.active_class != defining_class
        ):
            return None, RuntimeError(
                name_token.position_start,
                name_token.position_end,
                f"Cannot access private static field '{method_name}'",
                context,
            )

        if visibility == "PROTECTED":
            allowed = False
            if context and context.active_class:
                if (
                    defining_class in context.active_class.mro
                    or context.active_class in defining_class.mro
                ):
                    allowed = True

            if not allowed:
                return None, RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot access protected static field '{method_name}'",
                    context,
                )

        self._method_cache[cache_key] = (
            value,
            visibility,
            defining_class,
            "field",
        )
        return value, None
