"""Syntax message and integer literal limit checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import expect_equal, expect_startswith, expect_true
from .outcome import evaluate


def _syntax_check(source, expected_first_line):
    def check():
        outcome = evaluate(source)
        expect_true(outcome.python_exception is None, f"no crash: {outcome.describe()}")
        expect_true(
            outcome.error is not None, f"an error is expected: {outcome.describe()}"
        )
        expect_startswith(
            outcome.first_line, expected_first_line, "first line of the error"
        )
        expect_equal(outcome.stdout, "", "nothing runs when parsing fails")

    return check


def _integer_literal_limits():
    too_many_digits = "PRINTLN " + "9" * (Settings.MAX_INT_STR_DIGITS + 1)
    too_many_bits = "PRINTLN 0x" + "f" * (Settings.MAX_INT_BITS // 4 + 2)
    message = "Invalid Syntax: Integer literal too large (exceeds integer size limit)"
    for label, source in (
        ("decimal digits", too_many_digits),
        ("hex bits", too_many_bits),
    ):
        outcome = evaluate(source)
        expect_equal(outcome.first_line, message, f"{label} over the limit")


def _integer_literal_at_the_limit_is_accepted():
    outcome = evaluate("LET n = 0x" + "f" * 1000 + "\nPRINTLN n > 0")
    expect_equal(
        (outcome.stdout, outcome.error), ("1\n", None), "a long but legal literal"
    )
