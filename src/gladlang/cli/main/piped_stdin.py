"""Run GladLang code from standard input."""

import sys

from gladlang.core.util.settings import Settings
from gladlang.core.util.runner import run


def run_piped_stdin():
    raw_source = sys.stdin.buffer.read(Settings.MAX_SOURCE_BYTES + 1)

    if len(raw_source) > Settings.MAX_SOURCE_BYTES:
        sys.stderr.write(
            f"Source too large. Maximum allowed: "
            f"{Settings.MAX_SOURCE_BYTES:,} bytes.\n"
        )
        sys.exit(1)

    source = raw_source.decode("utf-8", errors="replace")

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
