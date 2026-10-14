"""REPL import and process checks."""

import os
import subprocess
import sys

from ..cli_support import (
    PROMPT,
    SOURCE_ROOT,
    Skip,
    expect_equal,
    expect_in,
    expect_not_in,
    expect_startswith,
    fail,
    run_python,
    welcome_banner,
)
from .drop_options import _drop


def _repl_import_over_constant_is_refused():
    files = {"m.glad": "EXPORT LET E = 2.71828\n"}
    body = _drop(["FINAL k = 1", 'IMPORT E AS k FROM "./m.glad"', "k + 0"], files)
    expect_in(
        "Runtime Error: Cannot redeclare 'k': it is a constant (FINAL)",
        body,
        "constants are protected",
    )
    expect_in(PROMPT + "1\n", body, "the constant keeps its value")


def _repl_import_may_rebind_a_variable():
    files = {"m.glad": "EXPORT LET E = 2.71828\n"}
    body = _drop(["LET v = 1", 'IMPORT E AS v FROM "./m.glad"', "v + 0"], files)
    expect_in(
        PROMPT + "2.71828\n",
        body,
        "re-importing over a plain variable is allowed in the REPL",
    )
    expect_not_in("Traceback", body, "no error")


def _repl_over_a_real_pipe():
    result = run_python(
        ["-c", "from gladlang.cli.main.repl import run_repl; run_repl()"],
        stdin=b"1 + 2\nexit\n",
    )
    expect_equal(result.returncode, 0, f"exit code ({result.describe()})")
    expect_equal(result.stderr, "", "stderr")
    expect_equal(
        result.stdout,
        welcome_banner() + PROMPT + "3\n" + PROMPT,
        "full transcript through a real process",
    )


def _repl_started_by_main_on_a_terminal():
    try:
        import pty
    except ImportError:
        raise Skip("pty module unavailable on this platform")

    master, slave = pty.openpty()
    try:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = SOURCE_ROOT
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONUTF8"] = "1"
        process = subprocess.Popen(
            [sys.executable, "-m", "gladlang"],
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
    finally:
        os.close(slave)

    try:
        os.write(master, b"1 + 2\nexit\n")
        stdout, stderr = process.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        fail("REPL did not exit after 'exit'")
    finally:
        os.close(master)

    text = stdout.decode("utf-8", errors="replace").replace("\r\n", "\n")
    expect_equal(process.returncode, 0, "exit code")
    expect_startswith(text, welcome_banner(), "terminal sessions start the REPL")
    expect_in(PROMPT + "3\n", text, "expression is evaluated")
