"""Command-line error checks."""

from ..cli_support import (
    expect_equal,
    expect_in,
    expect_startswith,
    run_cli,
    temporary_directory,
)
from .support import _failed, _write


def _input_without_data_fails():
    with temporary_directory() as directory:
        _write(directory, "need.glad", "LET a = INPUT()\nPRINTLN a\n")
        result = run_cli(["need.glad"], cwd=directory)
        _failed(result, "INPUT with closed stdin")
        expect_in("end of file reached", result.stderr, "diagnostic")


def _runtime_error_in_file():
    with temporary_directory() as directory:
        _write(directory, "boom.glad", "LET x = 1 / 0\n")
        result = run_cli(["boom.glad"], cwd=directory)
        _failed(result, "runtime error")
        expect_startswith(
            result.stderr, "Traceback (most recent call last):\n", "traceback header"
        )
        expect_in("boom.glad, line 1", result.stderr, "location names the file")
        expect_in("Runtime Error: Division by zero", result.stderr, "message")


def _runtime_error_inline():
    result = run_cli(["PRINTLN 1 / 0"])
    _failed(result, "inline runtime error")
    expect_in("File <cmdline>, line 1", result.stderr, "inline source name")
    expect_in("Runtime Error: Division by zero", result.stderr, "message")


def _syntax_error_inline():
    result = run_cli(["PRINTLN ("])
    _failed(result, "syntax error")
    expect_startswith(result.stderr, "Invalid Syntax:", "diagnostic kind")
    expect_in("File <cmdline>, line 1", result.stderr, "location")


def _uncaught_throw():
    result = run_cli(['THROW "boom"'])
    _failed(result, "uncaught THROW")
    expect_in("Runtime Error: boom", result.stderr, "message")
    expect_in("Thrown value: boom", result.stderr, "thrown value")


def _output_before_error_is_kept():
    result = run_cli(['PRINTLN "before"\nPRINTLN 1 / 0'])
    expect_equal(result.returncode, 1, "exit code")
    expect_equal(result.stdout, "before\n", "earlier output is preserved")
    expect_in("Division by zero", result.stderr, "error still reported")


def _missing_script_file():
    with temporary_directory() as directory:
        result = run_cli(["missing.glad"], cwd=directory)
        _failed(result, "missing file")
        expect_startswith(result.stderr, "Error accessing file:", "diagnostic")
        expect_in("missing.glad", result.stderr, "names the file")


def _directory_argument_is_rejected():
    with temporary_directory() as directory:
        (directory / "folder").mkdir()
        result = run_cli(["folder"], cwd=directory)
        _failed(result, "directory argument")
        expect_startswith(result.stderr, "Error accessing file:", "diagnostic")
