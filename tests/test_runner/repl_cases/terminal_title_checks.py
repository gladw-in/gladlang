"""Terminal title checks."""

import os
import sys

from ..cli_support import Skip, expect_equal


def _terminal_title():
    if os.name == "nt":
        raise Skip("terminal title uses the Windows console API on this platform")

    from gladlang.core.util.terminal import set_terminal_title

    class Stream:
        def __init__(self, is_terminal, fail_on_write=False):
            self.is_terminal = is_terminal
            self.fail_on_write = fail_on_write
            self.written = []

        def isatty(self):
            return self.is_terminal

        def write(self, text):
            if self.fail_on_write:
                raise OSError("closed")

            self.written.append(text)

    original = sys.stdout

    try:
        quiet = Stream(False)
        sys.stdout = quiet
        set_terminal_title("Title")
        expect_equal(
            quiet.written, [], "nothing is written when stdout is not a terminal"
        )

        terminal = Stream(True)
        sys.stdout = terminal
        set_terminal_title("Title")
        expect_equal(terminal.written, ["\033]0;Title\007"], "xterm title sequence")

        sys.stdout = Stream(True, fail_on_write=True)
        set_terminal_title("Title")
    finally:
        sys.stdout = original
