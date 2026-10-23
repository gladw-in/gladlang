"""Decides whether a test file passed from its output and error."""

import sys

from .data import EXPECTED_FAILURES, EXPECTED_OUTPUT_SUBSTRINGS
from .golden import compare_error, compare_stdout
from .helpers import has_explicit_test_failure


def judge_test_output(
    test_name,
    test_output,
    execution_error,
    passed_count,
    failed_count,
    failure_list,
):
    golden_problems = []
    stdout_problem = compare_stdout("top_level", test_name, test_output)
    if stdout_problem:
        golden_problems.append("Whole stdout mismatch:\n" + stdout_problem)

    if execution_error and EXPECTED_FAILURES.get(test_name) is not None:
        error_problem = compare_error(
            "top_level", test_name, execution_error.as_string()
        )
        if error_problem:
            golden_problems.append("Complete diagnostic mismatch:\n" + error_problem)

    if golden_problems:
        failed_count += 1
        failure_list.append((test_name, "\n\n".join(golden_problems)))
        sys.stdout.write("FAIL (golden mismatch)\n")
        return passed_count, failed_count, failure_list

    missing_outputs = [
        expected
        for expected in EXPECTED_OUTPUT_SUBSTRINGS.get(test_name, [])
        if expected not in test_output
    ]

    if missing_outputs:
        failed_count += 1
        failure_list.append(
            (
                test_name,
                "Missing expected output:\n" + "\n".join(missing_outputs),
            )
        )

        sys.stdout.write("FAIL (output mismatch)\n")
        return passed_count, failed_count, failure_list

    explicit_test_failure = has_explicit_test_failure(test_output)
    expected_error = EXPECTED_FAILURES.get(test_name)

    if execution_error:
        if expected_error is not None:
            actual_error = execution_error.as_string()
            if expected_error not in actual_error:
                failed_count += 1
                failure_list.append(
                    (
                        test_name,
                        f"Wrong error.\nExpected substring: {expected_error}\nActual error:\n{actual_error}",
                    )
                )
                sys.stdout.write("FAIL (wrong error)\n")
            elif explicit_test_failure:
                failed_count += 1
                failure_list.append(
                    (
                        test_name,
                        "Expected error occurred, but the test also reported an explicit failure",
                    )
                )
                sys.stdout.write("FAIL\n")
            else:
                passed_count += 1
                sys.stdout.write("PASS (expected error)\n")
        else:
            failed_count += 1
            failure_list.append((test_name, execution_error.as_string()))
            sys.stdout.write("FAIL\n")
    else:
        if expected_error is not None:
            failed_count += 1
            failure_list.append(
                (test_name, f"Expected error containing: {expected_error}")
            )
            sys.stdout.write("FAIL (expected error not raised)\n")
        elif explicit_test_failure:
            failed_count += 1
            failure_list.append(
                (test_name, "Test output explicitly reported a failure")
            )
            sys.stdout.write("FAIL (test assertion reported failure)\n")
        else:
            passed_count += 1
            sys.stdout.write("PASS\n")

    return passed_count, failed_count, failure_list
