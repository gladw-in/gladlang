"""Builds execution context for a function call in the TCO trampoline, enforcing recursion limits."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult


class FunctionSetupCallContext:
    __slots__ = ()

    def _setup_call_context(self, current_function, calling_context, base_depth):
        new_context = current_function.generate_new_context(
            calling_context if base_depth is None else None
        )

        new_context.active_class = getattr(current_function, "defining_class", None)
        new_context.is_static = getattr(current_function, "is_static", False)

        if hasattr(current_function, "_call_count"):
            current_function._call_count += 1

            if current_function._call_count > Settings.MAX_TOTAL_RECURSION:
                self._call_count = 0

                if (
                    hasattr(current_function, "_call_count")
                    and current_function is not self
                ):
                    current_function._call_count = 0

                return (
                    None,
                    base_depth,
                    RuntimeResult().failure(
                        RuntimeError(
                            current_function.position_start,
                            current_function.position_end,
                            f"Total recursion calls exceeded limit ({Settings.MAX_TOTAL_RECURSION})",
                            new_context,
                        )
                    ),
                )

        if base_depth is None:
            base_depth = new_context.depth
            new_context.parent_entry_position = self.position_start

        if new_context.depth > Settings.MAX_CONTEXT_DEPTH:
            self._reset_call_counts(current_function)

            return (
                None,
                base_depth,
                RuntimeResult().failure(
                    RuntimeError(
                        current_function.position_start,
                        current_function.position_end,
                        "Recursion limit exceeded",
                        new_context,
                    )
                ),
            )

        new_context._tco_func = current_function

        return new_context, base_depth, None
