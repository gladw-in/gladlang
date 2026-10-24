"""Runs builtin non-finite cases with exact expected stdout assertions."""

import io
import sys

from .builtin_nonfinite_cases import NONFINITE_CASES

from gladlang.core.util.runner import run
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.runtime.context import Context
from gladlang.values.primitives.number import Number

from .golden import normalize_line_endings
from .helpers import has_explicit_test_failure


def run_nonfinite_cases(passed_count, failed_count, failure_list):
    for case_name, source_code, expected_output in NONFINITE_CASES:
        display_name = f"builtin_nonfinite::{case_name}"
        sys.stdout.write(f"\n\nRunning {display_name}... \n")
        sys.stdout.flush()

        try:
            context = Context(f"<nonfinite:{case_name}>")
            context.symbol_table = get_fresh_global_scope()
            context.symbol_table.set("INF_VALUE", Number(float("inf")))
            captured_output = io.StringIO()

            original_stdout = sys.stdout

            try:
                sys.stdout = captured_output
                _, execution_error = run(
                    f"<nonfinite:{case_name}>",
                    source_code,
                    context,
                    instruction_limit=None,
                )
            finally:
                sys.stdout = original_stdout

            output = captured_output.getvalue()
            sys.stdout.write(output)
            problems = []

            actual_normalized = normalize_line_endings(output)
            expected_normalized = normalize_line_endings(expected_output)
            if actual_normalized != expected_normalized:
                problems.append(
                    "Whole stdout mismatch:\n"
                    f"Expected repr: {expected_normalized!r}\n"
                    f"Actual repr:   {actual_normalized!r}"
                )

            if execution_error:
                problems.append(
                    "Unexpected uncaught runtime error:\n" + execution_error.as_string()
                )
            if has_explicit_test_failure(output):
                problems.append("Case reported an explicit failure marker")

            if problems:
                failed_count += 1
                failure_list.append((display_name, "\n\n".join(problems)))
                sys.stdout.write("FAIL (assertion mismatch)\n")
            else:
                passed_count += 1
                sys.stdout.write("PASS (whole output and expected behavior verified)\n")
        except Exception as exception:
            failed_count += 1
            failure_list.append((display_name, str(exception)))
            sys.stdout.write("CRASH\n")

    return passed_count, failed_count, failure_list
