"""Build the execution context for one call in the TCO trampoline with recursion limits."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult


class BoundMethodSetupCallContext:
    __slots__ = ()

    def _setup_call_context(
        self,
        current_function,
        calling_context,
        base_depth,
        logical_parent_context,
        call_position_start,
        call_position_end,
    ):
        new_context = current_function.generate_new_context(
            calling_context if base_depth is None else None
        )

        new_context.active_class = getattr(current_function, "defining_class", None)
        new_context.is_static = getattr(current_function, "is_static", False)

        new_context.is_function_call_context = True
        new_context.logical_parent = logical_parent_context
        new_context.logical_parent_entry_position = call_position_start

        self._call_count += 1

        if self._call_count > Settings.MAX_TOTAL_RECURSION:
            self._call_count = 0
            return (
                None,
                base_depth,
                RuntimeResult().failure(
                    RuntimeError(
                        call_position_start,
                        call_position_end,
                        f"Total recursion calls exceeded limit ({Settings.MAX_TOTAL_RECURSION})",
                        new_context,
                    )
                ),
            )

        if base_depth is None:
            base_depth = new_context.depth
            new_context.parent_entry_position = self.position_start

        if new_context.depth > Settings.MAX_CONTEXT_DEPTH:
            self._call_count = 0
            return (
                None,
                base_depth,
                RuntimeResult().failure(
                    RuntimeError(
                        call_position_start,
                        call_position_end,
                        "Recursion limit exceeded",
                        new_context,
                    )
                ),
            )

        new_context._tail_call_function = current_function

        return new_context, base_depth, None
