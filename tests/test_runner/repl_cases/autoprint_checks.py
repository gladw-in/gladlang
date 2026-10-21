"""REPL autoprint checks."""

import io
import sys

from ..cli_support import expect_equal


class _Value:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


def _printed(source, text="VALUE"):
    from gladlang.cli.main.repl_autoprint import maybe_print_result

    original = sys.stdout
    captured = io.StringIO()
    sys.stdout = captured

    try:
        maybe_print_result(source, _Value(text))
    finally:
        sys.stdout = original

    return captured.getvalue()


def _autoprint_prints_expressions():
    for source in (
        "1 + 2",
        '"hello"',
        "x == 1",
        "x <= 1",
        "x >= 1",
        "x != 1",
        "foo() + 1",
        "1 + 2 # trailing comment",
        "[1, 2]",
        "a and b",
    ):
        expect_equal(_printed(source), "VALUE\n", f"{source!r} is echoed")


def _autoprint_suppresses_statements():
    suppressed = [
        "x = 5",
        "x += 1",
        "x -= 1",
        "x *= 2",
        "x /= 2",
        "x %= 2",
        "x //= 2",
        "x **= 2",
        "x &= 1",
        "x |= 1",
        "x ^= 1",
        "x <<= 1",
        "x >>= 1",
        "nums[0] = 1",
        "obj.attr = 2",
        "LET x = 1",
        "FINAL y = 2",
        "PRINTLN 1",
        "PRINT 1",
        "IF x THEN",
        "ELSE",
        "ENDIF",
        "WHILE x",
        "FOR i IN xs",
        "FUNC f()",
        "CLASS A",
        "RETURN 1",
        "THROW 1",
        "BREAK",
        "CONTINUE",
        "TRY",
        "x++",
        "++x",
        "x--",
        "--x",
        "foo()",
        "obj.run(1)",
        "# only a comment",
        "",
    ]

    for source in suppressed:
        expect_equal(_printed(source), "", f"{source!r} prints nothing")


def _autoprint_ignores_multi_line_input():
    expect_equal(_printed("1 + 1\n2 + 2"), "", "multi-line input is never echoed")


def _autoprint_uses_str_of_value():
    expect_equal(_printed("1 + 1", "custom text"), "custom text\n", "uses str(value)")
