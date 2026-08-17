"""Class attribute lookup with caching and MRO resolution."""

from gladlang.core.errors import RuntimeError


class ClassGetAttribute:
    __slots__ = ()

    def get_attribute(self, name_token, context=None, allow_instance=False):
        method_name = name_token.value

        cache_key = (method_name, allow_instance)

        if cache_key in self._method_cache:
            return self._get_attribute_from_cache(
                cache_key, method_name, name_token, context
            )

        lookup_result = self._get_attribute_lookup_mro(
            method_name, name_token, context, cache_key, allow_instance
        )

        if lookup_result is not None:
            return lookup_result

        return self._get_attribute_not_found(
            method_name, name_token, context, allow_instance
        )

    def _get_attribute_lookup_mro(
        self, method_name, name_token, context, cache_key, allow_instance
    ):
        for current_class in self.mro:
            result = self._try_static_field(
                current_class, method_name, name_token, context, cache_key
            )
            if result is not None:
                return result

            result = self._try_method_attribute(
                current_class,
                method_name,
                name_token,
                context,
                cache_key,
                allow_instance,
            )
            if result is not None:
                return result

        return None

    def _get_attribute_not_found(
        self, method_name, name_token, context, allow_instance
    ):
        if allow_instance:
            return None, RuntimeError(
                name_token.position_start,
                name_token.position_end,
                f"Instance of '{self.name}' has no attribute '{method_name}'",
                context,
            )

        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Class '{self.name}' has no member '{method_name}'",
            context,
        )
