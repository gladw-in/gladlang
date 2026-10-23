"""Prints the coverage audit summary and collects coverage problems."""

import sys

from .data import REGRESSION_EXPECTED_FAILURES


def write_audit_summary(audit):
    asserted_test_names = audit.asserted_test_names
    empty_assertion_names = audit.empty_assertion_names
    error_asserted_names = audit.error_asserted_names
    error_regression_files = audit.error_regression_files
    error_top_files = audit.error_top_files
    expected_inline_error_names = audit.expected_inline_error_names
    expected_token_error_names = audit.expected_token_error_names
    inline_error_map = audit.inline_error_map
    output_regression_files = audit.output_regression_files
    output_top_files = audit.output_top_files
    regression_names = audit.regression_names
    stale_error = audit.stale_error
    stale_output = audit.stale_output
    token_error_map = audit.token_error_map
    top_level_test_names = audit.top_level_test_names
    uncovered = audit.uncovered

    sys.stdout.write(
        f"\nWhole stdout golden fixtures present: "
        f"{len(output_top_files & top_level_test_names)}/{len(top_level_test_names)} top-level tests; "
        f"{len(output_regression_files & regression_names)}/{len(regression_names)} regressions\n"
    )
    sys.stdout.write(
        f"Complete diagnostic fixtures present: "
        f"{len(error_top_files & error_asserted_names)}/{len(error_asserted_names)} top-level expected-error cases; "
        f"{len(error_regression_files & set(REGRESSION_EXPECTED_FAILURES))}/{len(REGRESSION_EXPECTED_FAILURES)} regression cases; "
        f"{len(inline_error_map)}/{len(expected_inline_error_names)} inline; "
        f"{len(token_error_map)}/{len(expected_token_error_names)} token-limit\n"
    )
    sys.stdout.write(
        f"Supplementary semantic output fragments: {len(asserted_test_names)} top-level tests; "
        f"expected-error anchors: {len(error_asserted_names)} top-level tests\n"
    )

    if empty_assertion_names:
        sys.stdout.write(
            "\nAssertions with empty or blank strings " "(ignored for coverage):\n"
        )

        for name in empty_assertion_names:
            sys.stdout.write(f"  - {name}\n")

    if uncovered:
        sys.stdout.write(
            "\nTests with no output and no expected-error assertion "
            "(review individually):\n"
        )

        for name in uncovered:
            sys.stdout.write(f"  - {name}\n")

    if stale_output:
        sys.stdout.write("\nOutput assertions for missing test files:\n")
        for name in stale_output:
            sys.stdout.write(f"  - {name}\n")

    if stale_error:
        sys.stdout.write("\nExpected-error assertions for missing test files:\n")
        for name in stale_error:
            sys.stdout.write(f"  - {name}\n")


def collect_coverage_problems(audit):
    empty_assertion_names = audit.empty_assertion_names
    missing_inline_errors = audit.missing_inline_errors
    missing_regression_errors = audit.missing_regression_errors
    missing_regression_stdout = audit.missing_regression_stdout
    missing_token_errors = audit.missing_token_errors
    missing_top_errors = audit.missing_top_errors
    missing_top_stdout = audit.missing_top_stdout
    stale_error = audit.stale_error
    stale_inline_errors = audit.stale_inline_errors
    stale_output = audit.stale_output
    stale_regression_errors = audit.stale_regression_errors
    stale_regression_stdout = audit.stale_regression_stdout
    stale_token_errors = audit.stale_token_errors
    stale_top_errors = audit.stale_top_errors
    stale_top_stdout = audit.stale_top_stdout

    coverage_problems = []
    if empty_assertion_names:
        coverage_problems.append(
            "Empty or invalid output assertion entries: "
            + ", ".join(empty_assertion_names)
        )

    if stale_output:
        coverage_problems.append(
            "Output assertions reference missing test files: " + ", ".join(stale_output)
        )

    if stale_error:
        coverage_problems.append(
            "Expected-error assertions reference missing test files: "
            + ", ".join(stale_error)
        )

    fixture_problems = []
    for label, names in (
        ("missing top-level stdout fixtures", missing_top_stdout),
        ("stale top-level stdout fixtures", stale_top_stdout),
        ("missing regression stdout fixtures", missing_regression_stdout),
        ("stale regression stdout fixtures", stale_regression_stdout),
        ("missing top-level complete-error fixtures", missing_top_errors),
        ("stale top-level complete-error fixtures", stale_top_errors),
        ("missing regression complete-error fixtures", missing_regression_errors),
        ("stale regression complete-error fixtures", stale_regression_errors),
        ("missing inline complete-error fixtures", missing_inline_errors),
        ("stale inline complete-error fixtures", stale_inline_errors),
        ("missing token-limit complete-error fixtures", missing_token_errors),
        ("stale token-limit complete-error fixtures", stale_token_errors),
    ):
        if names:
            fixture_problems.append(f"{label}: " + ", ".join(names))

    if fixture_problems:
        coverage_problems.extend(fixture_problems)

    return coverage_problems
