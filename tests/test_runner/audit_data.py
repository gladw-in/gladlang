"""Collects the coverage audit data for the test suites."""

from types import SimpleNamespace

from pathlib import Path

from .data import (
    EXPECTED_FAILURES,
    EXPECTED_OUTPUT_SUBSTRINGS,
    REGRESSION_EXPECTED_FAILURES,
)
from .golden import GOLDEN_ROOT, load_diagnostic_map
from .lexer_syntax_regressions import REGRESSION_CASES
from .token_limit_regressions import TOKEN_LIMIT_CASES


def compute_audit(test_files, regression_files):
    top_level_test_names = {Path(path).name for path in test_files}

    asserted_output_entries = {
        name
        for name, expected in EXPECTED_OUTPUT_SUBSTRINGS.items()
        if expected and all(isinstance(item, str) and item.strip() for item in expected)
    }

    empty_assertion_names = sorted(
        name
        for name, expected in EXPECTED_OUTPUT_SUBSTRINGS.items()
        if not expected
        or not all(isinstance(item, str) and item.strip() for item in expected)
    )

    stale_output = sorted(asserted_output_entries - top_level_test_names)
    asserted_test_names = asserted_output_entries & top_level_test_names

    error_asserted_entries = set(EXPECTED_FAILURES)
    stale_error = sorted(error_asserted_entries - top_level_test_names)
    error_asserted_names = error_asserted_entries & top_level_test_names

    covered = asserted_test_names | error_asserted_names
    uncovered = sorted(top_level_test_names - covered)

    regression_names = {path.name for path in regression_files}
    output_top_files = {
        path.name[: -len(".stdout")]
        for path in (GOLDEN_ROOT / "top_level").glob("*.stdout")
    }
    output_regression_files = {
        path.name[: -len(".stdout")]
        for path in (GOLDEN_ROOT / "regression").glob("*.stdout")
    }
    error_top_files = {
        path.name[: -len(".error")]
        for path in (GOLDEN_ROOT / "top_level").glob("*.error")
    }
    error_regression_files = {
        path.name[: -len(".error")]
        for path in (GOLDEN_ROOT / "regression").glob("*.error")
    }
    missing_top_stdout = sorted(top_level_test_names - output_top_files)
    stale_top_stdout = sorted(output_top_files - top_level_test_names)
    missing_regression_stdout = sorted(regression_names - output_regression_files)
    stale_regression_stdout = sorted(output_regression_files - regression_names)
    missing_top_errors = sorted(error_asserted_names - error_top_files)
    stale_top_errors = sorted(error_top_files - error_asserted_names)
    missing_regression_errors = sorted(
        set(REGRESSION_EXPECTED_FAILURES) - error_regression_files
    )
    stale_regression_errors = sorted(
        error_regression_files - set(REGRESSION_EXPECTED_FAILURES)
    )

    expected_inline_error_names = {name for name, _, _ in REGRESSION_CASES}
    inline_error_map = load_diagnostic_map("inline_errors.json")
    missing_inline_errors = sorted(expected_inline_error_names - set(inline_error_map))
    stale_inline_errors = sorted(set(inline_error_map) - expected_inline_error_names)
    expected_token_error_names = {
        name for name, _, _, _, expected in TOKEN_LIMIT_CASES if expected is not None
    }
    token_error_map = load_diagnostic_map("token_limit_errors.json")
    missing_token_errors = sorted(expected_token_error_names - set(token_error_map))
    stale_token_errors = sorted(set(token_error_map) - expected_token_error_names)

    return SimpleNamespace(
        asserted_test_names=asserted_test_names,
        empty_assertion_names=empty_assertion_names,
        error_asserted_names=error_asserted_names,
        error_regression_files=error_regression_files,
        error_top_files=error_top_files,
        expected_inline_error_names=expected_inline_error_names,
        expected_token_error_names=expected_token_error_names,
        inline_error_map=inline_error_map,
        missing_inline_errors=missing_inline_errors,
        missing_regression_errors=missing_regression_errors,
        missing_regression_stdout=missing_regression_stdout,
        missing_token_errors=missing_token_errors,
        missing_top_errors=missing_top_errors,
        missing_top_stdout=missing_top_stdout,
        output_regression_files=output_regression_files,
        output_top_files=output_top_files,
        regression_names=regression_names,
        stale_error=stale_error,
        stale_inline_errors=stale_inline_errors,
        stale_output=stale_output,
        stale_regression_errors=stale_regression_errors,
        stale_regression_stdout=stale_regression_stdout,
        stale_token_errors=stale_token_errors,
        stale_top_errors=stale_top_errors,
        stale_top_stdout=stale_top_stdout,
        token_error_map=token_error_map,
        top_level_test_names=top_level_test_names,
        uncovered=uncovered,
    )
