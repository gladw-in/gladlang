"""Helpers that drive the REPL with scripted input."""

import io
import sys

from .assertions import expect_startswith
from .filesystem import working_directory


class ScriptedStdin:
    def __init__(self, steps):
        self.steps = list(steps)

    def readline(self):
        if not self.steps:
            return ""

        step = self.steps.pop(0)

        if isinstance(step, BaseException) or (
            isinstance(step, type) and issubclass(step, BaseException)
        ):
            raise step

        return step


WELCOME_BANNER = (
    "Welcome to GladLang (v{version})\n"
    "Type 'exit' or 'quit' to close the shell.\n"
    "--------------------------------------------------\n"
)


PROMPT = "GladLang > "


CONTINUATION = "...        > "


def welcome_banner():
    from gladlang.core.util.settings import Settings

    return WELCOME_BANNER.format(version=Settings.VERSION)


def run_repl_session(lines=None, stdin=None, directory=None):
    from gladlang.cli.main.repl import run_repl

    if stdin is None:
        stdin = io.StringIO("".join(line + "\n" for line in (lines or [])))

    original_stdin, original_stdout = sys.stdin, sys.stdout
    captured = io.StringIO()
    sys.stdin, sys.stdout = stdin, captured

    try:
        if directory is not None:
            with working_directory(directory):
                run_repl()
        else:
            run_repl()
    finally:
        sys.stdin, sys.stdout = original_stdin, original_stdout

    return captured.getvalue().replace("\r\n", "\n")


def repl_body(lines=None, stdin=None, directory=None):
    output = run_repl_session(lines=lines, stdin=stdin, directory=directory)
    banner = welcome_banner()
    expect_startswith(output, banner, "REPL must start with the welcome banner")
    return output[len(banner) :]
