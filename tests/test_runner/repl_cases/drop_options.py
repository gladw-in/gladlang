"""Dropped file option checks."""

from ..cli_support import PROMPT, expect_equal, repl_body, temporary_directory
from .support import EOF_TAIL, _lines, _write


def _drop(lines, files=None, binary_files=None, setup=None):
    with temporary_directory() as directory:
        for name, text in (files or {}).items():
            _write(directory, name, text)

        for name, data in (binary_files or {}).items():
            (directory / name).write_bytes(data)

        if setup:
            setup(directory)

        return repl_body(_lines(*lines), directory=directory)


OK_FILE = {"ok.glad": 'PRINTLN "from file"\n'}


def _dropped_file_auto_confirm():
    expect_equal(
        _drop(["ok.glad -y"], OK_FILE),
        PROMPT + "Running 'ok.glad'...\nfrom file\n" + EOF_TAIL,
        "-y runs the file without asking",
    )


def _dropped_file_flags_are_case_insensitive_and_long():
    for flag in ("-Y", "-yes", "-YES"):
        expect_equal(
            _drop([f"ok.glad {flag}"], OK_FILE),
            PROMPT + "Running 'ok.glad'...\nfrom file\n" + EOF_TAIL,
            f"{flag} confirms",
        )


def _dropped_file_confirmation_yes():
    expect_equal(
        _drop(["ok.glad", "y"], OK_FILE),
        PROMPT
        + "Run 'ok.glad' (20 bytes)? [y/n] Running 'ok.glad'...\nfrom file\n"
        + EOF_TAIL,
        "answering y runs the file",
    )


def _dropped_file_confirmation_declined():
    for answer in ("n", "", "yes please", "N"):
        expect_equal(
            _drop(["ok.glad", answer], OK_FILE),
            PROMPT + "Run 'ok.glad' (20 bytes)? [y/n] Cancelled by user.\n" + EOF_TAIL,
            f"answer {answer!r} cancels",
        )


def _dropped_file_auto_deny():
    for flag in ("-n", "-no", "-NO"):
        expect_equal(
            _drop([f"ok.glad {flag}"], OK_FILE),
            PROMPT + "Cancelled by user.\n" + EOF_TAIL,
            f"{flag} cancels without asking",
        )


def _dropped_file_deny_beats_confirm():
    expect_equal(
        _drop(["ok.glad -y -n"], OK_FILE),
        PROMPT + "Cancelled by user.\n" + EOF_TAIL,
        "-n wins when both flags are given",
    )


def _dropped_file_quoted_path():
    expect_equal(
        _drop(['"ok.glad" -y'], OK_FILE),
        PROMPT + "Running 'ok.glad'...\nfrom file\n" + EOF_TAIL,
        "surrounding quotes are stripped",
    )


def _dropped_file_arguments_feed_input():
    files = {"args.glad": "LET a = INPUT()\nLET b = INPUT()\nPRINTLN a + b\n"}
    expect_equal(
        _drop(["args.glad one two -y"], files),
        PROMPT + "Running 'args.glad'...\nonetwo\n" + EOF_TAIL,
        "positional tokens become INPUT() lines",
    )
