"""Visibility check for method access: PRIVATE and PROTECTED rules."""

from gladlang.core.errors import RuntimeError


class ClassGetAttributeMethodVisibility:
    __slots__ = ()

    def _check_method_visibility(self, method, method_name, name_token, context):
        visibility = method.visibility
        defining_class = method.defining_class

        if visibility == "PRIVATE" and (
            not context or context.active_class != defining_class
        ):
            return RuntimeError(
                name_token.position_start,
                name_token.position_end,
                f"Cannot access private method '{method_name}' via Class",
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
                return RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot access protected method '{method_name}' via Class",
                    context,
                )

        return None
