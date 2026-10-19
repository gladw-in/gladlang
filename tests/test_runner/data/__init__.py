"""Expected outputs, inputs, and error substrings used by the test runner."""

from .failures import EXPECTED_FAILURES, REGRESSION_EXPECTED_FAILURES
from .inputs import INPUT_MAP
from .output_substrings import EXPECTED_OUTPUT_SUBSTRINGS

__all__ = [
    "INPUT_MAP",
    "EXPECTED_OUTPUT_SUBSTRINGS",
    "EXPECTED_FAILURES",
    "REGRESSION_EXPECTED_FAILURES",
]
