"""Run GladLang scripts or code strings from the command line."""

import io
import sys

from gladlang.core.util.settings import Settings
from gladlang.core.util.runner import run

from .script_source import resolve_script_source


def run_script_mode():
    first_argument = sys.argv[1]

    if first_argument == "--help" or first_argument == "-h":
        sys.stdout.write(f"{Settings.HELP}\n")
        return

    if first_argument == "--version" or first_argument == "-v":
        sys.stdout.write(f"GladLang v{Settings.VERSION}\n")
        return

    source_argument = first_argument
    script_arguments = sys.argv[2:]
    try:
        original_stdin = sys.stdin
        try:
            if script_arguments:
                sys.stdin = io.StringIO("\n".join(script_arguments) + "\n")

            source_code, source_name = resolve_script_source(source_argument)

            result, error = run(
                source_name, source_code, instruction_limit=Settings.MAX_INSTRUCTIONS
            )

            if error:
                sys.stderr.write(f"{error.as_string()}\n")

        finally:
            sys.stdin = original_stdin

    except MemoryError:
        sys.stderr.write("System Error: Memory Limit Exceeded\n")
    except FileNotFoundError:
        sys.stderr.write(f"File not found: '{source_argument}'\n")
    except Exception as exception:
        sys.stderr.write(f"An unexpected error occurred: {exception}\n")
