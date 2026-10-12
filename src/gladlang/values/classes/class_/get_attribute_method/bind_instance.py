"""Binds an instance method to THIS when compatible, else returns an unbound copy."""


class ClassGetAttributeMethodBindInstance:
    __slots__ = ()

    def _bind_instance_method(
        self, method, context, cache_key, visibility, defining_class
    ):
        self._method_cache[cache_key] = (
            method.copy(),
            visibility,
            defining_class,
            "method",
        )

        if context:
            from gladlang.values.classes.instance_ import Instance

            instance = context.symbol_table.get("THIS")

            if (
                instance
                and isinstance(instance, Instance)
                and self in instance.class_reference.mro
            ):
                return method.copy().bind_to_instance(instance), None

        return method.copy(), None
