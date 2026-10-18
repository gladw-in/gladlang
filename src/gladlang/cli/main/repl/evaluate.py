"""Runs a complete buffered REPL input and prints the outcome."""

import sys

from gladlang.core.util.settings import Settings
from gladlang.core.util.runner import run

from ..repl_autoprint import maybe_print_result


def evaluate_complete_buffer(buffer, repl_context):
    result, error = run(
        "<stdin>",
        buffer,
        repl_context,
        instruction_limit=Settings.MAX_INSTRUCTIONS,
    )

    if error:
        sys.stdout.write(error.as_string() + "\n")
    elif result is not None:
        maybe_print_result(buffer, result)
