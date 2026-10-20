"""Basic command-line checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import expect_equal, run_cli, temporary_directory
from .support import _ok, _write


def _help_wins_over_extra_arguments():
    result = run_cli(["--help", "ignored.glad"])
    _ok(result, "--help with extra args")
    expect_equal(result.stdout, f"{Settings.HELP}\n", "help text")


def _inline_code():
    result = run_cli(['PRINTLN "inline"'])
    _ok(result, "inline code")
    expect_equal(result.stdout, "inline\n", "output")


def _inline_multi_statement():
    result = run_cli(["LET a = 2\nPRINTLN a * 21"])
    _ok(result, "inline multi-statement")
    expect_equal(result.stdout, "42\n", "output")


def _script_file_relative_and_absolute():
    with temporary_directory() as directory:
        script = _write(directory, "ok.glad", 'PRINTLN "from file"\n')
        relative = run_cli(["ok.glad"], cwd=directory)
        _ok(relative, "relative path")
        expect_equal(relative.stdout, "from file\n", "relative output")
        absolute = run_cli([str(script)], cwd=directory.parent)
        _ok(absolute, "absolute path")
        expect_equal(absolute.stdout, "from file\n", "absolute output")


def _existing_file_without_glad_extension_runs():
    with temporary_directory() as directory:
        _write(directory, "program.txt", 'PRINTLN "txt"\n')
        result = run_cli(["program.txt"], cwd=directory)
        _ok(result, "non-.glad file")
        expect_equal(result.stdout, "txt\n", "output")


def _unicode_output():
    with temporary_directory() as directory:
        _write(directory, "uni.glad", 'PRINTLN "வணக்கம்"\n')
        result = run_cli(["uni.glad"], cwd=directory)
        _ok(result, "unicode")
        expect_equal(result.stdout, "வணக்கம்\n", "output")


def _script_arguments_feed_input():
    with temporary_directory() as directory:
        _write(
            directory,
            "args.glad",
            'LET a = INPUT()\nLET b = INPUT()\nPRINTLN a + "-" + b\n',
        )
        result = run_cli(["args.glad", "first", "second"], cwd=directory)
        _ok(result, "two arguments")
        expect_equal(result.stdout, "first-second\n", "arguments are read by INPUT()")
