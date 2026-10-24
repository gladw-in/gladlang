"""Runs the main *.glad test suite."""

import glob
import io
import sys
from pathlib import Path

from gladlang.core.util.runner import run
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.runtime.context import Context

from .data import INPUT_MAP
from .file_verdict import judge_test_output
from .helpers import read_file_safe, time_limit, TestTimeout

TEST_TIMEOUT_SECONDS = 60


def run_test_files(test_dir, passed_count, failed_count, failure_list):
    test_files = sorted(glob.glob(str(test_dir / "*.glad")))

    for test_path in test_files:
        test_name = Path(test_path).name
        sys.stdout.write(f"\n\nRunning {test_name}... \n")
        sys.stdout.flush()

        original_stdin = sys.stdin
        input_data = INPUT_MAP.get(test_name)

        if input_data:
            sys.stdin = io.StringIO(input_data)

        try:
            source_code, read_error = read_file_safe(test_path)
            if read_error:
                raise RuntimeError(read_error)

            context = Context("<test>")
            context.symbol_table = get_fresh_global_scope()

            captured_output = io.StringIO()
            original_stdout = sys.stdout

            try:
                sys.stdout = captured_output
                with time_limit(TEST_TIMEOUT_SECONDS):
                    _, execution_error = run(
                        str(test_path), source_code, context, instruction_limit=None
                    )
            finally:
                sys.stdout = original_stdout

            test_output = captured_output.getvalue()
            sys.stdout.write(test_output)

            passed_count, failed_count, failure_list = judge_test_output(
                test_name,
                test_output,
                execution_error,
                passed_count,
                failed_count,
                failure_list,
            )

        except TestTimeout as exception:
            failed_count += 1
            failure_list.append((test_name, str(exception)))
            sys.stdout.write("TIMEOUT\n")
        except Exception as exception:
            failed_count += 1
            failure_list.append((test_name, str(exception)))
            sys.stdout.write("CRASH\n")
        finally:
            sys.stdin = original_stdin

    return passed_count, failed_count, failure_list
