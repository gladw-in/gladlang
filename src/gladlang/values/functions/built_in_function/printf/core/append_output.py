"""PRINTF output appending and size checking."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class BuiltInFunctionPrintfCoreAppendOutput:
    __slots__ = ()

    def _append_printf_text(self, output_parts, output_length, text, call_context):
        output_parts.append(text)
        output_length += len(text)
        if output_length > Settings.MAX_STRING_SIZE:
            return output_length, RuntimeError(
                self.position_start,
                self.position_end,
                f"PRINTF output exceeds maximum allowed size ({Settings.MAX_STRING_SIZE:,} chars)",
                call_context,
            )

        return output_length, None
