"""Check MRO class for method match with visibility and binding."""


class ClassGetAttributeMethodCore:
    __slots__ = ()

    def _try_method_attribute(
        self, current_class, method_name, name_token, context, cache_key, allow_instance
    ):
        method = current_class.methods.get(method_name)
        if not method:
            return None

        visibility = method.visibility
        defining_class = method.defining_class

        visibility_error = self._check_method_visibility(
            method, method_name, name_token, context
        )

        if visibility_error:
            return None, visibility_error

        if method.is_static:
            return self._bind_static_method(
                method, name_token, cache_key, visibility, defining_class
            )

        instance_error = self._check_instance_call_allowed(
            method_name, name_token, context, allow_instance
        )

        if instance_error:
            return None, instance_error

        return self._bind_instance_method(
            method, context, cache_key, visibility, defining_class
        )
