"""Expected error substrings for test and regression files."""

EXPECTED_FAILURES = {
    "test_arg_error.glad": "Incorrect argument count for 'add'",
    "test_assignments.glad": "Division by zero",
    "test_attr_error.glad": "has no attribute 'age'",
    "test_call_error.glad": "Illegal operation",
    "test_casting.glad": "Cannot convert 'hello' to INT",
    "test_invalid_float_literal_positive.glad": "Floating-point literal is not finite",
    "test_invalid_float_literal_negative.glad": "Floating-point literal is not finite",
    "test_module_error.glad": "has no export 'internal_helper'",
    "test_module_export_error.glad": "EXPORT can only be used inside a module",
    "test_name_error.glad": "'b' is not defined",
    "test_runtime_error.glad": "Division by zero",
    "test_syntax_error.glad": "Expected ')'",
    "test_syntax_error_paren.glad": "Expected ')'",
    "test_syntax_error_bracket.glad": "Expected ',' or ']'",
    "test_syntax_error_call.glad": "Expected ',' or ')'",
    "test_try_catch.glad": "Unhandled exception",
}


REGRESSION_EXPECTED_FAILURES = {
    "02_numeric_literals.glad": "Invalid numeric literal",
    "03_strings_templates.glad": "Invalid \\u escape",
    "04_collections.glad": "List index must be an integer",
    "05_functions.glad": "Overload conflict",
    "06_duplicate_arguments.glad": "Duplicate function argument 'a'",
    "07_this_parameter.glad": "'THIS' is reserved and cannot be used as a parameter name",
    "11_collision.glad": "already defined as a static field",
    "12_inherited_collision.glad": "already defined as a static field",
    "13_final.glad": "Cannot shadow constant 'x'",
    "15_tco_traceback.glad": "'missing_variable' is not defined",
    "16_numeric_literal_underscores.glad": "Invalid numeric literal",
    "17_radix_underscore_placement.glad": "Invalid hex literal",
    "18_enum_fractional_autoincrement.glad": "Enum values must be integers",
    "19_overload_visibility_mismatch.glad": "same static/instance mode",
    "20_decimal_underscore_before_digit.glad": "Invalid numeric literal",
    "21_bitwise_not_fractional.glad": "Operand must be an integer",
}
