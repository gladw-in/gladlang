"""Utilities for strict whole-output and complete-diagnostic assertions."""

import difflib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_ROOT = REPO_ROOT / "tests" / "expected_output"

DYNAMIC_TOKENS = {
    "{{INTEGER}}": r"[+-]?\d+",
    "{{NUMBER}}": r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
}


def normalize_line_endings(value):
    return value.replace("\r\n", "\n").replace("\r", "\n")


def normalize_diagnostic(value):
    value = value.replace(str(REPO_ROOT), "$REPO")
    value = value.replace(REPO_ROOT.as_posix(), "$REPO")
    value = re.sub(
        r"\$REPO[^,\r\n]*",
        lambda match: match.group(0).replace("\\", "/"),
        value,
    )

    return normalize_line_endings(value)


def read_fixture(path):
    return path.read_bytes().decode("utf-8")


def _output_pattern(expected):
    escaped = re.escape(expected)
    for token, pattern in DYNAMIC_TOKENS.items():
        escaped = escaped.replace(re.escape(token), pattern)

    return re.compile(escaped, re.DOTALL)


def _diff(expected, actual, expected_label, actual_label):
    diff = "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile=expected_label,
            tofile=actual_label,
        )
    )

    if not diff:
        return (
            f"Expected {len(expected)} characters; got {len(actual)} characters. "
            f"Expected repr: {expected!r}\nActual repr: {actual!r}"
        )

    return diff


def compare_stdout(section, test_name, actual):
    fixture_path = GOLDEN_ROOT / section / f"{test_name}.stdout"
    if not fixture_path.is_file():
        return f"Missing whole-output golden fixture: {fixture_path.relative_to(REPO_ROOT)}"

    expected = normalize_line_endings(read_fixture(fixture_path))
    actual = normalize_line_endings(actual)
    if _output_pattern(expected).fullmatch(actual):
        return None

    return _diff(
        expected,
        actual,
        str(fixture_path.relative_to(REPO_ROOT)),
        f"actual stdout for {test_name}",
    )


def compare_error(section, test_name, actual_error):
    fixture_path = GOLDEN_ROOT / section / f"{test_name}.error"

    if not fixture_path.is_file():
        return (
            "Missing complete-diagnostic golden fixture: "
            f"{fixture_path.relative_to(REPO_ROOT)}"
        )

    expected = normalize_diagnostic(read_fixture(fixture_path))
    actual = normalize_diagnostic(actual_error)

    if actual == expected:
        return None

    return _diff(
        expected,
        actual,
        str(fixture_path.relative_to(REPO_ROOT)),
        f"actual diagnostic for {test_name}",
    )


def compare_inline_diagnostic(expected, actual, label):
    expected = normalize_diagnostic(expected)
    actual = normalize_diagnostic(actual)

    if actual == expected:
        return None

    return _diff(
        expected,
        actual,
        f"golden diagnostic for {label}",
        f"actual diagnostic for {label}",
    )


def load_diagnostic_map(filename):
    fixture_path = GOLDEN_ROOT / filename
    if not fixture_path.is_file():
        raise FileNotFoundError(f"Missing diagnostic fixture: {fixture_path}")

    return json.loads(read_fixture(fixture_path))
