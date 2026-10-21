"""Checks that pin known issues as expected failures."""

from ..cli_support import (
    expect_equal,
    expect_startswith,
    expect_true,
    temporary_directory,
)
from .module_path_checks import _module_layout, _resolve
from .outcome import evaluate


def _type_survives_copy_with_equality():
    outcome = evaluate("PRINTLN [Number][0:1][0] == Number")
    expect_equal(
        outcome.stdout,
        "1\n",
        f"a type compared with itself after copying ({outcome.describe()})",
    )


def _instanceof_message_does_not_blame_a_valid_right_operand():
    outcome = evaluate("PRINTLN Number INSTANCEOF Number")
    expect_true(
        "Right operand of INSTANCEOF" not in (outcome.error or ""),
        f"the right operand is a valid type ({outcome.describe()})",
    )


def _bare_println_on_its_own_line():
    outcome = evaluate('PRINTLN\nPRINTLN "x"')
    expect_equal(
        (outcome.stdout, outcome.error),
        ("\nx\n", None),
        "bare PRINTLN prints a blank line",
    )


def _empty_interpolation_is_a_syntax_error():
    outcome = evaluate("PRINTLN `a ${} b`")
    expect_startswith(
        outcome.first_line or "",
        "Invalid Syntax",
        f"empty ${{}} ({outcome.describe()})",
    )


def _missing_file_outside_the_root_gives_the_same_error():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        existing = _resolve("../outside/o.glad", root)[0]
        missing = _resolve("../outside/nothing.glad", root)[0]
        expect_equal(missing, existing, "both must report the same confinement error")


def _null_on_the_left_is_guarded_like_on_the_right():
    right = evaluate("PRINTLN 1 + NULL")
    left = evaluate("PRINTLN NULL + 1")
    expect_true(right.error is not None, "1 + NULL raises today")
    expect_true(
        left.error is not None, f"NULL + 1 should raise too ({left.describe()})"
    )


BIG_FLOAT_MIX = "LET a = 2 ** 1000\nLET b = a * a\n"


def _huge_integer_with_float(expression):
    def check():
        outcome = evaluate(BIG_FLOAT_MIX + f'LET r = {expression}\nPRINTLN "ok"')
        expect_true(
            outcome.python_exception is None,
            f"must be a GladLang error, not a Python crash ({outcome.python_exception})",
        )
        expect_true(outcome.error is not None, "an overflow error is expected")

    return check


def _module_operation_must_not_crash(statement):
    def check():
        with temporary_directory() as directory:
            (directory / "m.glad").write_text(
                "EXPORT LET PI = 3.14\n", encoding="utf-8"
            )
            source = 'IMPORT * AS m FROM "./m.glad"\n' + statement + '\nPRINTLN "done"'
            outcome = evaluate(source, entry_path=directory / "entry.glad")

        expect_true(
            outcome.python_exception is None,
            f"must be a GladLang result, not a Python crash ({outcome.python_exception})",
        )

    return check


MODULE_ISSUE = "Module values lack position_start/context, so these operations crash with an AttributeError"
