"""Access SUPER.method by searching MRO from start_class with visibility checks."""

from gladlang.core.errors import RuntimeError


class SuperGetAttribute:
    __slots__ = ()

    def get_attribute(self, name_token, context=None):
        method_name = name_token.value
        mro = self.instance.class_reference.mro

        try:
            start_index = mro.index(self.start_class) + 1
        except ValueError:
            return None, RuntimeError(
                name_token.position_start,
                name_token.position_end,
                "Current class not found in MRO",
                context,
            )

        for index in range(start_index, len(mro)):
            current_class = mro[index]
            found_method = current_class.methods.get(method_name)
            if found_method:
                visibility = found_method.visibility
                defining_class = found_method.defining_class
                if visibility == "PRIVATE" and (
                    not context or context.active_class != defining_class
                ):
                    return None, RuntimeError(
                        name_token.position_start,
                        name_token.position_end,
                        f"Cannot access private method '{method_name}' via SUPER",
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
                            f"Cannot access protected method '{method_name}' via SUPER",
                            context,
                        )

                return found_method.copy().bind_to_instance(self.instance), None

        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Method '{method_name}' not found in superclasses",
            context,
        )
