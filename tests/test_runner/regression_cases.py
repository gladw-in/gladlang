"""Runs the inline lexer/syntax regression cases."""

import sys

from .lexer_syntax_regressions import REGRESSION_CASES, REGRESSION_EXPECTED_ERRORS

from .helpers import run_source
from .golden import compare_inline_diagnostic, load_diagnostic_map


def run_regression_cases(passed_count, failed_count, failure_list):
    complete_expected_errors = load_diagnostic_map("inline_errors.json")
    for case_name, source_code, description in REGRESSION_CASES:
        display_name = f"lexer_syntax_regressions::{case_name}"
        expected_error = REGRESSION_EXPECTED_ERRORS[case_name]
        complete_expected_error = complete_expected_errors.get(case_name)

        sys.stdout.write(f"\n\nRunning {display_name}... \n")
        sys.stdout.flush()

        try:
            execution_error = run_source(case_name, source_code)

            if execution_error is None:
                failed_count += 1
                failure_list.append(
                    (display_name, f"Expected error containing: {expected_error}")
                )
                sys.stdout.write("FAIL (expected error not raised)\n")
            else:
                actual_error = execution_error.as_string()
                problems = []

                if expected_error not in actual_error:
                    problems.append(
                        f"Expected error fragment not found: {expected_error!r}"
                    )

                if complete_expected_error is None:
                    problems.append("Missing complete diagnostic fixture")
                else:
                    mismatch = compare_inline_diagnostic(
                        complete_expected_error, actual_error, case_name
                    )
                    if mismatch:
                        problems.append("Complete diagnostic mismatch:\n" + mismatch)

                if problems:
                    failed_count += 1
                    failure_list.append((display_name, "\n\n".join(problems)))
                    sys.stdout.write("FAIL (wrong error)\n")
                else:
                    passed_count += 1
                    sys.stdout.write("PASS (complete diagnostic verified)\n")

        except Exception as exception:
            failed_count += 1
            failure_list.append((display_name, str(exception)))
            sys.stdout.write("CRASH\n")

    return passed_count, failed_count, failure_list
