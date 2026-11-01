"""Test runner package – sets up sys.path and exposes the main() entry point."""

import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = PACKAGE_DIR.parent
REPO_ROOT = SCRIPTS_DIR.parent
TEST_ROOT = REPO_ROOT / "tests"

for candidate in (REPO_ROOT / "src", TEST_ROOT, SCRIPTS_DIR):
    candidate_string = str(candidate)
    if candidate_string not in sys.path:
        sys.path.insert(0, candidate_string)

if hasattr(sys, "set_int_max_str_digits"):
    from gladlang.core.util.settings import Settings

    sys.set_int_max_str_digits(Settings.MAX_INT_STR_DIGITS)

if hasattr(sys, "setrecursionlimit"):
    from gladlang.core.util.settings import Settings

    sys.setrecursionlimit(Settings.PYTHON_RECURSION_LIMIT)

from .main import main

__all__ = ["main"]
