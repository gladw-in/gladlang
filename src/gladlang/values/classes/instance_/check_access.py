"""Shared visibility check helper."""

from gladlang.core.errors import RuntimeError


class InstanceCheckAccess:
    def check_access(self, name_token, visibility, defining_class, context):
        if visibility == "PUBLIC":
            return None

        if visibility == "PRIVATE":
            if not context or context.active_class != defining_class:
                return RuntimeError(
                    name_token.position_start,
                    name_token.position_end,
                    f"Cannot access private member '{name_token.value}'",
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
                    f"Cannot access protected member '{name_token.value}'",
                    context,
                )

        return None
