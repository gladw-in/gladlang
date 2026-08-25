import glob
import sys
import os
import io
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gladlang.core.util.runner import run
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.settings import Settings
from gladlang.runtime.context import Context

INPUT_MAP = {
    "test_calculator.glad": "10\n20\n",
    "test_casting.glad": "123.5\n",
    "test_input.glad": "Glad\nGlad\n",
    "test_input_math.glad": "Glad\n10\n20\n",
    "test_builtins.glad": "Glad\n",
}

EXPECTED_FAILURES = {
    "test_arg_error.glad",
    "test_assignments.glad",
    "test_attr_error.glad",
    "test_call_error.glad",
    "test_casting.glad",
    "test_name_error.glad",
    "test_recursion.glad",
    "test_runtime_error.glad",
    "test_syntax_error.glad",
    "test_try_catch.glad",
}


def read_file_safe(path):
    try:
        O_NOFOLLOW = os.O_NOFOLLOW
        file_descriptor = os.open(str(path), os.O_RDONLY | O_NOFOLLOW)
    except AttributeError:
        file_descriptor = os.open(str(path), os.O_RDONLY)

    try:
        file_size = os.fstat(file_descriptor).st_size
        if file_size > Settings.MAX_SOURCE_BYTES:
            os.close(file_descriptor)
            return (
                None,
                f"File too large: {file_size:,} bytes (max {Settings.MAX_SOURCE_BYTES:,})",
            )

        file_handle = os.fdopen(file_descriptor, "r", encoding="utf-8")

        try:
            return file_handle.read(), None
        except UnicodeDecodeError:
            return None, f"File is not valid UTF-8: {Path(path).name}"
        finally:
            file_handle.close()
    except Exception:
        os.close(file_descriptor)
        raise


def main():
    test_dir = Path(__file__).parent.parent / "tests"
    test_files = sorted(glob.glob(str(test_dir / "*.glad")))

    if not test_files:
        sys.stderr.write("No test files found!\n")
        sys.exit(1)

    passed_count = 0
    failed_count = 0
    failure_list = []

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

            execution_context = Context("<test>")
            execution_context.symbol_table = get_fresh_global_scope()

            _, execution_error = run(
                str(test_path),
                source_code,
                execution_context,
                instruction_limit=None,
            )

            if execution_error:
                if test_name in EXPECTED_FAILURES:
                    passed_count += 1
                    sys.stdout.write("PASS (expected error)\n")
                else:
                    failed_count += 1
                    failure_list.append((test_name, execution_error.as_string()))
                    sys.stdout.write("FAIL\n")
            else:
                if test_name in EXPECTED_FAILURES:
                    failed_count += 1
                    failure_list.append((test_name, "Expected error but got success"))
                    sys.stdout.write("FAIL (expected error not raised)\n")
                else:
                    passed_count += 1
                    sys.stdout.write("PASS\n")

        except Exception as exception:
            failed_count += 1
            failure_list.append((test_name, str(exception)))
            sys.stdout.write("CRASH\n")
        finally:
            sys.stdin = original_stdin

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


if __name__ == "__main__":
    main()
