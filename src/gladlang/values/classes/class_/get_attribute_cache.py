"""Fast revalidate visibility for cached get_attribute lookups."""

from gladlang.core.errors import RuntimeError
from gladlang.values.functions.base_function import BaseFunction
from gladlang.values.functions.bound_method import BoundMethod


class ClassGetAttributeCache:
    __slots__ = ()

    def _get_attribute_from_cache(self, cache_key, method_name, name_token, context):
        (
            cached_value,
            cached_visibility,
            cached_defining_class,
            cached_kind,
        ) = self._method_cache[cache_key]

        def _check_visibility(visibility, defining_class, kind):
            if visibility == "PRIVATE":
                if (
                    not context
                    or not context.active_class
                    or context.active_class != defining_class
                ):
                    message = (
                        f"Cannot access private static field '{method_name}'"
                        if kind == "field"
                        else f"Cannot access private method '{method_name}' via Class"
                    )
                    return RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        message,
                        context,
                    )

            elif visibility == "PROTECTED":
                allowed = False
                if context and context.active_class:
                    if (
                        defining_class in context.active_class.mro
                        or context.active_class in defining_class.mro
                    ):
                        allowed = True

                if not allowed:
                    message = (
                        f"Cannot access protected static field '{method_name}'"
                        if kind == "field"
                        else f"Cannot access protected method '{method_name}' via Class"
                    )
                    return RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        message,
                        context,
                    )

            return None

        error = _check_visibility(cached_visibility, cached_defining_class, cached_kind)
        if error:
            return None, error

        if isinstance(cached_value, (BaseFunction, BoundMethod)):
            return cached_value.copy(), None

        return cached_value, None
