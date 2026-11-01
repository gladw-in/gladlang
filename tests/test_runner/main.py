"""Orchestrates all test suites and prints the final summary."""

import glob
import sys
from pathlib import Path

from .audit_data import compute_audit
from .audit_report import collect_coverage_problems, write_audit_summary
from .class_copy_check import run_class_copy_check
from .cli_cases import run_cli_cases
from .language_cases import run_language_cases
from .nonfinite_cases import run_nonfinite_cases
from .regression_cases import run_regression_cases
from .regression_files import run_regression_files
from .repl_cases import run_repl_cases
from .test_files import run_test_files
from .token_limits import run_token_limit_cases


def _force_utf8_output():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def main():
    _force_utf8_output()
    test_dir = Path(__file__).resolve().parent.parent.parent / "tests"
    regression_dir = test_dir / "regression"

    test_files = sorted(glob.glob(str(test_dir / "*.glad")))
    regression_files = sorted(regression_dir.glob("*.glad"))

    if not test_files and not regression_files:
        sys.stderr.write("No test files found!\n")
        sys.stderr.write(f"Looked in: {test_dir}\n")
        sys.stderr.write(f"Regression dir: {regression_dir}\n")
        sys.exit(1)

    audit = compute_audit(test_files, regression_files)
    write_audit_summary(audit)

    passed_count = 0
    failed_count = 0
    failure_list = []

    coverage_problems = collect_coverage_problems(audit)
    if coverage_problems:
        failed_count += 1
        failure_list.append(("coverage_audit", "\n".join(coverage_problems)))

    passed_count, failed_count, failure_list = run_test_files(
        test_dir, passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_regression_files(
        regression_files, passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_regression_cases(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_nonfinite_cases(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_token_limit_cases(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_class_copy_check(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_cli_cases(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_repl_cases(
        passed_count, failed_count, failure_list
    )

    passed_count, failed_count, failure_list = run_language_cases(
        passed_count, failed_count, failure_list
    )

    sys.stdout.write("\n" + "=" * 50 + "\n")
    total_tests = passed_count + failed_count
    sys.stdout.write(f"Tests:   {total_tests}\n")
    sys.stdout.write(f"Passed:  {passed_count}\n")
    sys.stdout.write(f"Failed:  {failed_count}\n")

    if failure_list:
        sys.stdout.write("\n--- Failures ---\n")
        for name, error_message in failure_list:
            sys.stdout.write(f"\n{name}:\n{error_message}\n")

        sys.exit(1)

    sys.stdout.write("\nAll tests passed!\n")
    sys.exit(0)
