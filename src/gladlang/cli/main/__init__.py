"""GladLang command-line interface and interactive REPL."""

import sys
import threading

from gladlang.core.util.settings import Settings

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(Settings.MAX_INT_STR_DIGITS)

if hasattr(sys, "setrecursionlimit"):
    sys.setrecursionlimit(Settings.PYTHON_RECURSION_LIMIT)

from gladlang.core.util.memory import set_memory_limit
from gladlang.core.util.terminal import set_terminal_title

from .piped_stdin import run_piped_stdin
from .repl import run_repl
from .script_mode import run_script_mode


def main():
    set_memory_limit(Settings.MAX_MEMORY_MB)

    threading.Thread(
        target=set_terminal_title, args=(Settings.TITLE,), daemon=True
    ).start()

    if len(sys.argv) == 1 and not sys.stdin.isatty():
        run_piped_stdin()
        return

    if len(sys.argv) == 1:
        run_repl()
    elif len(sys.argv) >= 2:
        run_script_mode()
    else:
        sys.stdout.write("Error: Invalid arguments.\n")
        sys.stdout.write(Settings.HELP + "\n")


__all__ = ["main"]
