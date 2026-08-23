"""Confirm and run a dropped .glad file in the REPL."""

import io
import sys

from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.settings import Settings
from gladlang.core.util.runner import run


def confirm_and_run_dropped_file(
    drop_path,
    dropped_source,
    resolved_path,
    file_size,
    arguments,
    auto_confirm,
    auto_deny,
    repl_context,
):
    if auto_deny:
        sys.stdout.write("Cancelled by user.\n")
        return True

    if not auto_confirm:
        sys.stdout.write(f"Run '{drop_path.name}' ({file_size:,} bytes)? [y/n] ")
        sys.stdout.flush()

        response = sys.stdin.readline().strip().lower()
        if response != "y":
            sys.stdout.write("Cancelled by user.\n")
            return True

    sys.stdout.write(f"Running '{drop_path.name}'...\n")

    original_stdin = sys.stdin
    try:
        if arguments:
            sys.stdin = io.StringIO("\n".join(arguments) + "\n")

        repl_context.symbol_table = get_fresh_global_scope()

        result, error = run(
            str(resolved_path),
            dropped_source,
            repl_context,
            instruction_limit=Settings.MAX_INSTRUCTIONS,
        )
    finally:
        sys.stdin = original_stdin

    if error:
        sys.stdout.write(error.as_string() + "\n")

    return True
