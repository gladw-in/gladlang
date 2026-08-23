"""Find nearest superclass constructor in MRO with visibility enforcement."""

from gladlang.core.errors import RuntimeError


class SuperFindConstructor:
    __slots__ = ()

    def _find_super_constructor(self, mro, start_index):
        for index in range(start_index, len(mro)):
            current_class = mro[index]
            if current_class.name in current_class.methods:
                constructor_method = current_class.methods[current_class.name]
                visibility = constructor_method.visibility
                defining_class = constructor_method.defining_class

                if visibility == "PRIVATE" and (
                    not self.context or self.context.active_class != defining_class
                ):
                    return None, RuntimeError(
                        self.position_start,
                        self.position_end,
                        f"Cannot access private constructor of '{current_class.name}' via SUPER",
                        self.context,
                    )

                if visibility == "PROTECTED":
                    allowed = False
                    if self.context and self.context.active_class:
                        if (
                            defining_class in self.context.active_class.mro
                            or self.context.active_class in defining_class.mro
                        ):
                            allowed = True

                    if not allowed:
                        return None, RuntimeError(
                            self.position_start,
                            self.position_end,
                            f"Cannot access protected constructor of '{current_class.name}' via SUPER",
                            self.context,
                        )

                return constructor_method, None

        return None, None
