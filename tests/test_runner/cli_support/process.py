"""Helpers that run GladLang in a subprocess."""

import os
import subprocess
import sys
from pathlib import Path

import gladlang

from .assertions import _short

SOURCE_ROOT = str(Path(gladlang.__file__).resolve().parent.parent)


SUBPROCESS_TIMEOUT_SECONDS = 60


class CliResult:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def describe(self):
        return (
            f"rc={self.returncode} stdout={_short(self.stdout)} "
            f"stderr={_short(self.stderr)}"
        )


def _subprocess_environment():
    environment = dict(os.environ)
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        SOURCE_ROOT if not existing else SOURCE_ROOT + os.pathsep + existing
    )
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONUTF8"] = "1"
    return environment


def _decode(data):
    return data.decode("utf-8", errors="replace").replace("\r\n", "\n")


def run_python(arguments, stdin=None, cwd=None):
    keyword_arguments = {}

    if stdin is None:
        keyword_arguments["stdin"] = subprocess.DEVNULL
    else:
        keyword_arguments["input"] = stdin

    completed = subprocess.run(
        [sys.executable, *arguments],
        capture_output=True,
        cwd=cwd,
        env=_subprocess_environment(),
        timeout=SUBPROCESS_TIMEOUT_SECONDS,
        **keyword_arguments,
    )

    return CliResult(
        completed.returncode, _decode(completed.stdout), _decode(completed.stderr)
    )


def run_cli(arguments, stdin=None, cwd=None):
    return run_python(["-m", "gladlang", *arguments], stdin=stdin, cwd=cwd)
