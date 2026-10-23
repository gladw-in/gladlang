"""REPL error and recovery checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import (
    CONTINUATION,
    PROMPT,
    ScriptedStdin,
    expect_equal,
    expect_in,
    expect_startswith,
    expect_true,
    repl_body,
)
from .support import EOF_TAIL, _lines


def _runtime_error_is_reported_and_state_survives():
    body = repl_body(_lines("LET x = 1", "1 / 0", "x + 41"))
    expect_equal(
        body,
        PROMPT
        + PROMPT
        + "Traceback (most recent call last):\n"
        + "  File <stdin>, line 1, in <repl>\n"
        + "Runtime Error: Division by zero\n"
        + PROMPT
        + "42\n"
        + EOF_TAIL,
        "traceback goes to stdout and the session keeps going",
    )


def _syntax_error_is_reported_and_session_continues():
    body = repl_body(_lines("1 +", "2 + 2"))
    expect_startswith(body, PROMPT + "Invalid Syntax:", "syntax error is reported")
    expect_in("File <stdin>, line", body, "a location is shown")
    expect_in(PROMPT + "4\n", body, "the next entry still works")


def _syntax_error_points_at_the_typed_line():
    body = repl_body(_lines("1 +"))
    expect_in("File <stdin>, line 1\n", body, "error is on the line the user typed")


def _undefined_name_error():
    body = repl_body(_lines("nothing_here + 1"))
    expect_in("Runtime Error: 'nothing_here' is not defined", body, "NameError text")


def _buffer_limit_clears_buffer():
    limit = Settings.MAX_REPL_BUFFER
    filler = "# " + "x" * 998
    count = limit // 1000 + 3
    body = repl_body(_lines("IF TRUE THEN", *([filler] * count), "1 + 1"))
    message = "Error: Input buffer limit exceeded. Clearing buffer.\n"
    expect_equal(body.count(message), 1, "limit message appears exactly once")
    expect_true(
        body.endswith("2\n" + EOF_TAIL), "session recovers and evaluates later input"
    )


def _keyboard_interrupt_discards_buffer():
    stdin = ScriptedStdin(["FUNC f()\n", KeyboardInterrupt, "1 + 1\n", "exit\n"])
    body = repl_body(stdin=stdin)
    expect_equal(
        body,
        PROMPT + CONTINUATION + "\nKeyboardInterrupt\n" + PROMPT + "2\n" + PROMPT,
        "Ctrl+C drops the half-typed block and continues",
    )


def _memory_error_is_reported_and_recovers():
    stdin = ScriptedStdin([MemoryError, "2 + 2\n", "exit\n"])
    expect_equal(
        repl_body(stdin=stdin),
        PROMPT + "System Error: Memory Limit Exceeded\n" + PROMPT + "4\n" + PROMPT,
        "MemoryError is reported without ending the shell",
    )


def _unexpected_exception_becomes_shell_error():
    stdin = ScriptedStdin([ValueError("boom"), "3 + 3\n", "exit\n"])
    expect_equal(
        repl_body(stdin=stdin),
        PROMPT + "Shell Error: boom\n" + PROMPT + "6\n" + PROMPT,
        "unexpected failures are reported and the shell continues",
    )


def _exit_inside_open_block_is_not_a_command():
    body = repl_body(_lines("FUNC f()", "exit", "ENDFUNC", "PRINTLN 7"))
    expect_equal(
        body,
        PROMPT + CONTINUATION * 2 + PROMPT + "7\n" + EOF_TAIL,
        "'exit' is block content while a block is open",
    )
