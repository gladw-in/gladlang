"""Runs the language-level checks."""

from ..cli_support import run_checks
from .check_list_core import CORE_CHECKS, SYNTAX_CHECKS
from .check_list_known import KNOWN_CHECKS
from .check_list_module import MODULE_CHECKS

LANGUAGE_CHECKS = SYNTAX_CHECKS + CORE_CHECKS + KNOWN_CHECKS + MODULE_CHECKS


def run_language_cases(passed_count, failed_count, failure_list):
    return run_checks(
        "language", LANGUAGE_CHECKS, passed_count, failed_count, failure_list
    )
