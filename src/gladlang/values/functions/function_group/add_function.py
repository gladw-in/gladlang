"""Registers a new overload variant into a FunctionGroup."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class FunctionGroupAddFunction:
    __slots__ = ()

    def add_function(self, new_variant):
        argument_count = len(new_variant.argument_names)

        if argument_count in self.functions:
            return RuntimeResult().failure(
                RuntimeError(
                    new_variant.position_start,
                    new_variant.position_end,
                    f"Overload conflict: '{self.name}' already has a variant with {argument_count} argument(s)",
                    None,
                )
            )

        self.functions[argument_count] = new_variant

        if len(self.functions) == 1:
            self.visibility = getattr(new_variant, "visibility", "PUBLIC")
            self.is_static = getattr(new_variant, "is_static", False)
            self.defining_class = getattr(new_variant, "defining_class", None)
        else:
            if getattr(new_variant, "visibility", "PUBLIC") != self.visibility:
                return RuntimeResult().failure(
                    RuntimeError(
                        new_variant.position_start,
                        new_variant.position_end,
                        f"All overloads of '{self.name}' must have the same visibility",
                        None,
                    )
                )

        return None
