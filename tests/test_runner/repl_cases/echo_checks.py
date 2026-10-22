"""REPL echo checks pinned as known issues."""

from ..cli_support import PROMPT, expect_equal, expect_in, repl_body
from .autoprint_checks import _printed
from .support import _lines

BARE_NAME_ISSUE = (
    "is_increment regex in repl_autoprint.py also matches plain names, "
    "so a bare name is never echoed"
)


def _bare_variable_is_echoed():
    expect_equal(_printed("x"), "VALUE\n", "typing a variable name shows its value")


def _indexing_is_echoed():
    expect_equal(_printed("nums[0]"), "VALUE\n", "typing nums[0] shows the element")


def _member_access_is_echoed():
    expect_equal(
        _printed("person.name"), "VALUE\n", "typing person.name shows the value"
    )


def _value_returning_call_is_echoed():
    body = repl_body(_lines("FUNC add(a, b)", "RETURN a + b", "ENDFUNC", "add(1, 2)"))
    expect_in(PROMPT + "3\n", body, "a call that returns a value shows it")
