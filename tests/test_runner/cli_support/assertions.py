"""Assertion helpers for the CLI and REPL checks."""


class Skip(Exception):
    pass


def fail(message):
    raise AssertionError(message)


def _short(value, limit=400):
    text = repr(value)
    if len(text) > limit:
        text = text[:limit] + f"... <{len(text)} chars>"

    return text


def expect_equal(actual, expected, label):
    if actual != expected:
        fail(f"{label}\n  expected: {_short(expected)}\n  actual:   {_short(actual)}")


def expect_true(condition, label):
    if not condition:
        fail(label)


def expect_in(needle, haystack, label):
    if needle not in haystack:
        fail(f"{label}\n  missing:  {_short(needle)}\n  in:       {_short(haystack)}")


def expect_not_in(needle, haystack, label):
    if needle in haystack:
        fail(
            f"{label}\n  unexpected: {_short(needle)}\n  in:         {_short(haystack)}"
        )


def expect_startswith(text, prefix, label):
    if not text.startswith(prefix):
        fail(
            f"{label}\n  expected prefix: {_short(prefix)}\n  actual:          {_short(text)}"
        )
