"""REPL tokenizer and call detection checks."""

from ..cli_support import expect_equal, expect_true


def _tokenize_cases():
    from gladlang.cli.main.repl_tokenize import tokenize_repl_line as tokenize

    cases = [
        ("", ("", [], False, False)),
        ("file.glad", ("file.glad", [], False, False)),
        ("file.glad a b", ("file.glad", ["a", "b"], False, False)),
        ("file.glad -y", ("file.glad", [], True, False)),
        ("file.glad -YES", ("file.glad", [], True, False)),
        ("file.glad -n", ("file.glad", [], False, True)),
        ("file.glad -No", ("file.glad", [], False, True)),
        ("file.glad -y -n", ("file.glad", [], True, True)),
        ("file.glad a -y b", ("file.glad", ["a", "b"], True, False)),
        ("file.glad --verbose x", ("file.glad", ["x"], False, False)),
        ('"my file.glad" -y', ("my file.glad", [], True, False)),
        ("'quoted.glad'", ("quoted.glad", [], False, False)),
        ('"unbalanced -y', ("unbalanced", [], True, False)),
    ]

    for line, expected in cases:
        expect_equal(tokenize(line), expected, f"tokenize({line!r})")


def _pure_call_detection():
    from gladlang.cli.main.repl_call_check import is_pure_call_expression as check

    expected_true = [
        "foo()",
        "foo(1, 2)",
        "obj.method()",
        "a.b.c(1)",
        "f(1).g(2)",
        'foo("a)b")',
        "foo(`x)y`)",
        "foo(bar(1))",
        "foo()[0]",
    ]

    expected_false = [
        "foo",
        "foo + 1",
        "foo() + 1",
        "1 + foo()",
        "x[0]",
        "x.y",
        "(1)",
        "",
        "foo() bar",
    ]

    for source in expected_true:
        expect_true(check(source), f"{source!r} is a pure call")

    for source in expected_false:
        expect_true(not check(source), f"{source!r} is not a pure call")
