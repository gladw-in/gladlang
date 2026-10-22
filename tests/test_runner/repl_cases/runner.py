"""Runs the REPL checks."""

from ..cli_support import run_checks
from .check_list_drop import DROP_CHECKS
from .check_list_helpers import HELPER_CHECKS
from .check_list_session import SESSION_CHECKS

REPL_CHECKS = SESSION_CHECKS + DROP_CHECKS + HELPER_CHECKS


def run_repl_cases(passed_count, failed_count, failure_list):
    return run_checks("repl", REPL_CHECKS, passed_count, failed_count, failure_list)
