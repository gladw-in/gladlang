"""Runtime error – includes traceback generation and thrown value support."""

from gladlang.core.util.settings import Settings

from .error import Error


class RuntimeError(Error):
    __slots__ = ("context", "thrown_value")

    def __init__(
        self, position_start, position_end, details, context, thrown_value=None
    ):
        super().__init__(position_start, position_end, "Runtime Error", details)
        self.context = context
        self.thrown_value = thrown_value

    def _sanitize_for_display(self, text):
        return "".join(
            (
                character
                if character == "\t" or character.isprintable()
                else f"\\x{ord(character):02x}"
            )
            for character in text
        )

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self._sanitize_for_display(self.details)}"

        if self.thrown_value is not None:
            result += (
                f"\nThrown value: "
                f"{self._sanitize_for_display(str(self.thrown_value))}"
            )

        return result

    def generate_traceback(self):
        traceback_frames = []

        position = self.position_start
        current_context = self.context

        seen_contexts = set()

        while current_context and id(current_context) not in seen_contexts:
            seen_contexts.add(id(current_context))

            if position is not None:
                traceback_frames.append(
                    f"  File {position.filename}, line {position.line + 1}, in {current_context.display_name}\n"
                )

            position = current_context.parent_entry_position
            current_context = current_context.parent

        if current_context:
            traceback_frames.append("  ... cyclic context chain detected ...\n")

        traceback_frames.reverse()

        if len(traceback_frames) > Settings.MAX_TRACEBACK_FRAMES:
            head_count = Settings.MAX_TRACEBACK_FRAMES // 2
            tail_count = Settings.MAX_TRACEBACK_FRAMES - head_count
            omitted_count = len(traceback_frames) - (head_count + tail_count)

            traceback_frames = (
                traceback_frames[:head_count]
                + [f"  ... {omitted_count} frames omitted ...\n"]
                + traceback_frames[-tail_count:]
            )

        if not traceback_frames:
            return ""

        return "Traceback (most recent call last):\n" + "".join(traceback_frames)
