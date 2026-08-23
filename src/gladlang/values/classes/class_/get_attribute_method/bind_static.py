"""Binds a static method as an unbound copy and caches the result."""


class ClassGetAttributeMethodBindStatic:
    __slots__ = ()

    def _bind_static_method(
        self, method, name_token, cache_key, visibility, defining_class
    ):
        result = (
            method.copy()
            .set_context(self.context)
            .set_position(name_token.position_start, name_token.position_end)
        )

        self._method_cache[cache_key] = (
            result,
            visibility,
            defining_class,
            "method",
        )

        return result, None
