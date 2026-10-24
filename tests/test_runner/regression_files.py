"""Runs ``tests/regression/*.glad`` with strict stdout/error golden checks."""

import io
import sys

from gladlang.core.util.runner import run
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.runtime.context import Context

from .data import REGRESSION_EXPECTED_FAILURES
from .golden import compare_error, compare_stdout
from .helpers import read_file_safe, has_explicit_test_failure


def run_regression_files(regression_files, passed_count, failed_count, failure_list):
    for regression_path in regression_files:
        regression_name = regression_path.name
        display_name = f"regression::{regression_name}"
        sys.stdout.write(f"\n\nRunning {display_name}... \n")
        sys.stdout.flush()

        try:
            source_code, read_error = read_file_safe(regression_path)
            if read_error:
                raise RuntimeError(read_error)

            context = Context(f"<regression:{regression_name}>")
            context.symbol_table = get_fresh_global_scope()
            captured_output = io.StringIO()

            original_stdout = sys.stdout

            try:
                sys.stdout = captured_output
                _, execution_error = run(
                    str(regression_path), source_code, context, instruction_limit=None
                )
            finally:
                sys.stdout = original_stdout

            output = captured_output.getvalue()
            sys.stdout.write(output)
            problems = []

            whole_output_problem = compare_stdout("regression", regression_name, output)
            if whole_output_problem:
                problems.append("Whole stdout mismatch:\n" + whole_output_problem)

            explicit_test_failure = has_explicit_test_failure(output)
            expected_error = REGRESSION_EXPECTED_FAILURES.get(regression_name)
            if execution_error:
                actual_error = execution_error.as_string()
                if expected_error is None:
                    problems.append("Unexpected execution error:\n" + actual_error)
                else:
                    if expected_error not in actual_error:
                        problems.append(
                            f"Expected error category/message fragment not found: {expected_error!r}\n"
                            f"Actual error:\n{actual_error}"
                        )

                    complete_error_problem = compare_error(
                        "regression", regression_name, actual_error
                    )

                    if complete_error_problem:
                        problems.append(
                            "Complete diagnostic mismatch:\n" + complete_error_problem
                        )

                    if explicit_test_failure:
                        problems.append(
                            "Expected error occurred, but regression output also reports failure"
                        )

            elif expected_error is not None:
                problems.append(
                    f"Expected error was not raised (expected: {expected_error})"
                )
            elif explicit_test_failure:
                problems.append("Regression output explicitly reported a failure")

            if problems:
                failed_count += 1
                failure_list.append((display_name, "\n\n".join(problems)))
                sys.stdout.write("FAIL (assertion mismatch)\n")
            else:
                passed_count += 1
                sys.stdout.write("PASS (whole output verified)\n")

        except Exception as exception:
            failed_count += 1
            failure_list.append((display_name, str(exception)))
            sys.stdout.write("CRASH\n")

    return passed_count, failed_count, failure_list
