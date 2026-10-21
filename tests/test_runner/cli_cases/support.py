"""Shared helpers for the CLI checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import expect_equal, expect_in, run_cli


def _ok(result, label):
    expect_equal(result.returncode, 0, f"{label}: exit code ({result.describe()})")
    expect_equal(result.stderr, "", f"{label}: stderr must be empty")


def _failed(result, label):
    expect_equal(result.returncode, 1, f"{label}: exit code ({result.describe()})")
    expect_equal(result.stdout, "", f"{label}: stdout must be empty")


def _write(directory, name, text):
    path = directory / name
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _version(flag):
    def check():
        result = run_cli([flag])
        _ok(result, flag)
        expect_equal(result.stdout, f"GladLang v{Settings.VERSION}\n", f"{flag} output")

    return check


def _help(flag):
    def check():
        result = run_cli([flag])
        _ok(result, flag)
        expect_equal(result.stdout, f"{Settings.HELP}\n", f"{flag} output")
        expect_in("Usage: gladlang", result.stdout, f"{flag} shows usage")

    return check
