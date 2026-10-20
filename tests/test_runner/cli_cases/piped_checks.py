"""Piped standard input checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import (
    expect_equal,
    expect_in,
    expect_not_in,
    expect_startswith,
    run_cli,
)
from .support import _failed, _ok


def _piped_stdin_runs_code():
    result = run_cli([], stdin=b'PRINTLN "piped"\n')
    _ok(result, "piped code")
    expect_equal(result.stdout, "piped\n", "output")
    expect_not_in("Welcome", result.stdout, "piped input must not start the REPL")


def _piped_empty_stdin():
    result = run_cli([], stdin=b"")
    _ok(result, "empty stdin")
    expect_equal(result.stdout, "", "no output")


def _piped_runtime_error():
    result = run_cli([], stdin=b"PRINTLN 1 / 0\n")
    _failed(result, "piped runtime error")
    expect_in("File <stdin>, line 1", result.stderr, "source name")


def _piped_syntax_error():
    result = run_cli([], stdin=b"PRINTLN (\n")
    _failed(result, "piped syntax error")
    expect_startswith(result.stderr, "Invalid Syntax:", "diagnostic kind")


def _piped_invalid_utf8_is_replaced():
    result = run_cli([], stdin=b'PRINTLN "a\xffb"\n')
    _ok(result, "piped invalid UTF-8")
    expect_equal(result.stdout, "a\ufffdb\n", "bad byte becomes U+FFFD")


def _piped_size_limit():
    limit = Settings.MAX_SOURCE_BYTES
    exact = run_cli([], stdin=b"#" + b"x" * (limit - 2) + b"\n")
    _ok(exact, "piped source of exactly the limit")

    over = run_cli([], stdin=b"#" + b"x" * (limit - 1) + b"\n")
    _failed(over, "piped source over the limit")
    expect_equal(
        over.stderr,
        f"Source too large. Maximum allowed: {limit:,} bytes.\n",
        "diagnostic",
    )
