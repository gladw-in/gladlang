"""Fallback attribute lookup: class methods and static members, with binding."""

from gladlang.core.errors import RuntimeError
from gladlang.values.functions.base_function import BaseFunction
from gladlang.values.functions.function import Function


class InstanceGetAttributeClassMember:
    def _get_attribute_class_member(self, name_token, context=None):
        name = name_token.value

        if context and context.active_class:
            method_object = context.active_class.methods.get(name)
            if method_object and method_object.visibility == "PRIVATE":
                return method_object.copy().bind_to_instance(self), None

        member_value, lookup_error = self.class_reference.get_attribute(
            name_token, context, allow_instance=True
        )

        if lookup_error:
            return None, lookup_error

        if isinstance(member_value, BaseFunction):
            if isinstance(member_value, Function) and member_value.is_static:
                return member_value, None

            if member_value.visibility == "PRIVATE":
                defining_class = member_value.defining_class
                allowed = False
                if context and context.active_class == defining_class:
                    allowed = True

                if not allowed:
                    return None, RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        f"Cannot access private method '{name_token.value}'",
                        context,
                    )

            if member_value.visibility == "PROTECTED":
                defining_class = getattr(member_value, "defining_class", None)
                allowed = False
                if context and context.active_class and defining_class:
                    if (
                        defining_class in context.active_class.mro
                        or context.active_class in defining_class.mro
                    ):
                        allowed = True

                if not allowed:
                    return None, RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        f"Cannot access protected method '{name_token.value}'",
                        context,
                    )

            bound_method = member_value.copy().bind_to_instance(self)
            return bound_method, None

        return member_value, None
