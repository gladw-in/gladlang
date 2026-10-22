"""Basic REPL session checks."""

from ..cli_support import (
    CONTINUATION,
    PROMPT,
    expect_equal,
    repl_body,
    run_repl_session,
    welcome_banner,
)
from .support import EOF_TAIL, EXIT_TAIL, _lines


def _banner_and_exit_command():
    expect_equal(
        run_repl_session(_lines("exit")),
        welcome_banner() + PROMPT,
        "banner, prompt, then a silent exit",
    )


def _exit_command_variants():
    for command in ("quit", "EXIT", "  Exit  ", "QuIt"):
        expect_equal(
            repl_body(_lines(command)), EXIT_TAIL, f"{command!r} must end the shell"
        )


def _eof_exits_cleanly():
    expect_equal(repl_body([]), EOF_TAIL, "end of input prints Exiting.")


def _expression_results_are_echoed():
    expect_equal(
        repl_body(_lines("1 + 2", '"a" + "b"', "[1, 2, 3]")),
        PROMPT + "3\n" + PROMPT + "ab\n" + PROMPT + "[1, 2, 3]\n" + EOF_TAIL,
        "numbers, strings and lists are echoed",
    )


def _comparison_expressions_are_echoed():
    body = repl_body(_lines("LET x = 1", "x == 1", "x <= 1", "x != 2"))
    expect_equal(
        body,
        PROMPT * 2 + "1\n" + PROMPT + "1\n" + PROMPT + "1\n" + EOF_TAIL,
        "comparisons are not mistaken for assignments",
    )


def _statements_are_not_echoed():
    body = repl_body(_lines("LET x = 5", "x = 6", "x += 4", "x++", "--x", "x + 0"))
    expect_equal(
        body,
        PROMPT * 5 + PROMPT + "10\n" + EOF_TAIL,
        "LET, assignment, compound assignment and ++/-- print nothing",
    )


def _print_statement_output_is_not_duplicated():
    expect_equal(
        repl_body(_lines('PRINTLN "hi"')),
        PROMPT + "hi\n" + EOF_TAIL,
        "PRINTLN prints once without echoing its return value",
    )


def _state_persists_between_lines():
    body = repl_body(
        _lines(
            "LET a = 20", "FUNC twice(n)", "RETURN n * 2", "ENDFUNC", "PRINTLN twice(a)"
        )
    )
    expect_equal(
        body,
        PROMPT + PROMPT + CONTINUATION * 2 + PROMPT + "40\n" + EOF_TAIL,
        "variables and functions survive across entries",
    )
