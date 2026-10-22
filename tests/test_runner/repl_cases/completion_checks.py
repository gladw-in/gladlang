"""REPL input completeness checks."""

from ..cli_support import expect_equal, expect_true


def _strip_helpers():
    from gladlang.core.util.repl_helpers.comment_strip import strip_comments
    from gladlang.core.util.repl_helpers.quote_stripping import strip_double_quoted

    quote_cases = [
        ('a "b" c', "a  c"),
        ('"a\\"b" x', " x"),
        ("a `t` c", "a  c"),
        ("`a\\`b` x", " x"),
        ('x "unterminated', "x "),
        ("no quotes", "no quotes"),
        ("", ""),
        ('"one" + "two"', " + "),
    ]

    for source, expected in quote_cases:
        expect_equal(
            strip_double_quoted(source), expected, f"strip_double_quoted({source!r})"
        )

    comment_cases = [
        ("a # b", "a "),
        ("a\nb # c\nd", "a\nb \nd"),
        ("# whole line", ""),
        ("no comment", "no comment"),
        ("", ""),
    ]

    for source, expected in comment_cases:
        expect_equal(strip_comments(source), expected, f"strip_comments({source!r})")


def _unterminated_multiline_detection():
    from gladlang.core.util.repl_helpers.unterminated_check import (
        has_unterminated_multiline as check,
    )

    open_cases = ['"""abc', 'x = """abc\ndef', "`abc", "`a\\`b", 'a """b """ c """']
    closed_cases = [
        '"""abc"""',
        "`abc`",
        "plain",
        "",
        '"single" line',
        '"""a""" """b"""',
    ]

    for source in open_cases:
        expect_true(check(source), f"{source!r} is unterminated")

    for source in closed_cases:
        expect_true(not check(source), f"{source!r} is complete")


def _is_complete_cases():
    from gladlang.core.util.repl_helpers import is_complete

    complete = [
        "1 + 2\n",
        "",
        "\n",
        "[1, 2]\n",
        '{"a": 1}\n',
        "IF x THEN\nENDIF\n",
        "IF a THEN\nELSE\nENDIF\n",
        "IF a THEN\nELSE IF b THEN\nELSE\nENDIF\n",
        "TRY\nCATCH e\nFINALLY\nENDTRY\n",
        "FUNC f()\nENDFUNC\n",
        "CLASS A\nFUNC f()\nENDFUNC\nENDCLASS\n",
        "ENUM E\nENDENUM\n",
        "SWITCH x\nENDSWITCH\n",
        "WHILE x\nENDWHILE\n",
        "FOR i IN xs\nENDFOR\n",
        'PRINTLN "IF FUNC CLASS"\n',
        "# IF FUNC CLASS\n",
        "LET IFX = 1\n",
        "LET xFUNC = 1\n",
        "[x FOR x IN [1, 2]]\n",
        '{k: v FOR k IN ["a"]}\n',
        'PRINTLN "unterminated\n',
        '"""abc"""\n',
        "`abc`\n",
        ")\n",
        "ENDIF\n",
    ]

    incomplete = [
        "PRINTLN (\n",
        "[1, 2\n",
        "{\n",
        "IF x THEN\n",
        "IF a THEN\nELSE\n",
        "TRY\nCATCH e\n",
        "FUNC f()\n",
        "CLASS A\nFUNC f()\nENDFUNC\n",
        "ENUM E\n",
        "SWITCH x\n",
        "WHILE x\n",
        "FOR i IN xs\n",
        "FOR i IN xs\nIF i THEN\nENDIF\n",
        '"""abc\n',
        "LET s = `abc\n",
        "`a\\`b\n",
        'PRINTLN "a" + (\n',
    ]

    for source in complete:
        expect_true(is_complete(source), f"{source!r} should be complete")

    for source in incomplete:
        expect_true(not is_complete(source), f"{source!r} should be incomplete")
