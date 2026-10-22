"""REPL multi-line input checks."""

from ..cli_support import CONTINUATION, PROMPT, expect_equal, repl_body
from .support import EOF_TAIL, _lines


def _multiline_block_uses_continuation_prompt():
    body = repl_body(
        _lines(
            "LET n = 3",
            "IF n > 1 THEN",
            'PRINTLN "big"',
            "ELSE",
            'PRINTLN "small"',
            "ENDIF",
        )
    )
    expect_equal(
        body,
        PROMPT * 2 + CONTINUATION * 4 + "big\n" + EOF_TAIL,
        "block is buffered until ENDIF, then runs once",
    )


def _nested_blocks_run_as_one_unit():
    body = repl_body(
        _lines("FOR i IN [1, 2]", "IF i > 0 THEN", "PRINTLN i", "ENDIF", "ENDFOR")
    )
    expect_equal(
        body,
        PROMPT + CONTINUATION * 4 + "1\n2\n" + EOF_TAIL,
        "nested FOR/IF completes at the outer ENDFOR",
    )


def _open_bracket_waits_for_more_input():
    body = repl_body(_lines("PRINTLN (", "1 + 1", ")"))
    expect_equal(
        body,
        PROMPT + CONTINUATION * 2 + "2\n" + EOF_TAIL,
        "an unclosed bracket continues onto the next line",
    )


def _triple_quoted_string_spans_lines():
    body = repl_body(_lines('LET s = """abc', 'def"""', "PRINTLN s"))
    expect_equal(
        body,
        PROMPT + CONTINUATION + PROMPT + "abc\ndef\n" + EOF_TAIL,
        "triple-quoted strings continue across lines",
    )


def _backtick_template_spans_lines():
    body = repl_body(_lines("LET t = `one", "two`", "PRINTLN t"))
    expect_equal(
        body,
        PROMPT + CONTINUATION + PROMPT + "one\ntwo\n" + EOF_TAIL,
        "backtick templates continue across lines",
    )


def _blank_lines_and_comments_are_ignored():
    body = repl_body(_lines("", "   ", "# only a comment", "1 + 1"))
    expect_equal(
        body,
        PROMPT * 3 + PROMPT + "2\n" + EOF_TAIL,
        "blank and comment-only entries produce no output",
    )


def _trailing_comment_does_not_hide_result():
    expect_equal(
        repl_body(_lines("1 + 1 # note")),
        PROMPT + "2\n" + EOF_TAIL,
        "result is still echoed",
    )
