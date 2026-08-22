"""Run GladLang code from standard input."""

import sys

from gladlang.core.util.settings import Settings
from gladlang.core.util.runner import run


def run_piped_stdin():
    source = sys.stdin.read()

    if len(source.encode("utf-8", errors="replace")) > Settings.MAX_SOURCE_BYTES:
        sys.stderr.write(
            f"Source too large ({len(source):,} chars). "
            f"Maximum allowed: {Settings.MAX_SOURCE_BYTES:,} bytes.\n"
        )
        sys.exit(1)

    try:
        result, error = run(
            "<stdin>", source, instruction_limit=Settings.MAX_INSTRUCTIONS
        )

        if error:
            sys.stderr.write(f"{error.as_string()}\n")
            sys.exit(1)
    except MemoryError:
        sys.stderr.write("System Error: Memory Limit Exceeded\n")
        sys.exit(1)
    except Exception as exception:
        sys.stderr.write(f"An unexpected error occurred: {exception}\n")
        sys.exit(1)
