"""Dispatches execute() by built-in function name to the appropriate handler."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class BuiltInFunctionDispatch:
    __slots__ = ()

    def execute(self, arguments, interpreter, calling_context=None):
        call_context = calling_context or self.context

        if self.name == "INPUT":
            return self._execute_input(arguments, call_context)
        elif self.name == "STR":
            return self._execute_str(arguments, call_context, calling_context)
        elif self.name == "INT":
            return self._execute_int(arguments, call_context, calling_context)
        elif self.name == "FLOAT":
            return self._execute_float(arguments, call_context, calling_context)
        elif self.name == "BOOL":
            return self._execute_bool(arguments, call_context, calling_context)
        elif self.name == "LEN":
            return self._execute_len(arguments, call_context, calling_context)
        elif self.name == "PRINTF":
            return self._execute_printf(arguments, call_context, calling_context)
        elif self.name == "TIME":
            return self._execute_time(arguments, call_context, calling_context)
        elif self.name == "TIME_SECONDS":
            return self._execute_time_seconds(arguments, call_context, calling_context)
        elif self.name == "TIME_MILLIS":
            return self._execute_time_millis(arguments, call_context, calling_context)
        elif self.name == "TIME_NANOS":
            return self._execute_time_nanos(arguments, call_context, calling_context)
        elif self.name == "RANDOM":
            return self._execute_random(arguments, call_context, calling_context)
        elif self.name == "RANDOM_FLOAT":
            return self._execute_random_float(arguments, call_context, calling_context)
        elif self.name == "RANDOM_RANGE":
            return self._execute_random_range(arguments, call_context, calling_context)
        elif self.name == "DELAY":
            return self._execute_delay(arguments, call_context, calling_context)

        return RuntimeResult().failure(
            RuntimeError(
                self.position_start,
                self.position_end,
                f"Unknown built-in function '{self.name}'",
                call_context,
            )
        )
