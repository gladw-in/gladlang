"""Runs token-limit regressions with complete diagnostic assertions."""

import sys

from .token_limit_regressions import TOKEN_LIMIT_CASES

from gladlang.core.util.settings import Settings
from gladlang.lexer import Lexer

from .golden import compare_inline_diagnostic, load_diagnostic_map


def run_token_limit_cases(passed_count, failed_count, failure_list):
    complete_expected_errors = load_diagnostic_map("token_limit_errors.json")
    for (
        case_name,
        source,
        token_limit,
        expected_count,
        expected_error,
    ) in TOKEN_LIMIT_CASES:
        display_name = f"token_limit::{case_name}"
        original_limit = Settings.MAX_TOKENS

        try:
            Settings.MAX_TOKENS = token_limit
            tokens, error = Lexer(display_name, source).make_tokens()
        except Exception as exception:
            tokens, error = None, exception
        finally:
            Settings.MAX_TOKENS = original_limit

        if expected_error is not None:
            actual_error = (
                (error.as_string() if hasattr(error, "as_string") else str(error))
                if error is not None
                else None
            )

            problems = []

            if actual_error is None:
                problems.append(f"Expected error was not raised: {expected_error}")
            elif expected_error not in actual_error:
                problems.append(
                    f"Expected error fragment not found: {expected_error!r}\n"
                    f"Actual diagnostic:\n{actual_error}"
                )

            complete_expected_error = complete_expected_errors.get(case_name)
            if complete_expected_error is None:
                problems.append("Missing complete token-limit diagnostic fixture")
            elif actual_error is not None:
                mismatch = compare_inline_diagnostic(
                    complete_expected_error, actual_error, display_name
                )
                if mismatch:
                    problems.append("Complete diagnostic mismatch:\n" + mismatch)

            if problems:
                failed_count += 1
                failure_list.append((display_name, "\n\n".join(problems)))
                sys.stdout.write(f"FAIL: {display_name}\n")
            else:
                passed_count += 1
                sys.stdout.write(
                    f"PASS: {display_name} (complete diagnostic verified)\n"
                )
        elif error is None and len(tokens) - 1 == expected_count:
            passed_count += 1
            sys.stdout.write(f"PASS: {display_name}\n")
        else:
            failed_count += 1
            actual_count = None if tokens is None else len(tokens) - 1
            failure_list.append(
                (
                    display_name,
                    f"Expected {expected_count} non-EOF tokens; got {actual_count}; error={error}",
                )
            )
            sys.stdout.write(f"FAIL: {display_name}\n")

    return passed_count, failed_count, failure_list
