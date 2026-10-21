"""Check list for known issues."""

from .known_issue_checks import (
    _bare_println_on_its_own_line,
    _empty_interpolation_is_a_syntax_error,
    _instanceof_message_does_not_blame_a_valid_right_operand,
    _missing_file_outside_the_root_gives_the_same_error,
    _null_on_the_left_is_guarded_like_on_the_right,
    _type_survives_copy_with_equality,
)

KNOWN_CHECKS = [
    (
        "known_type_survives_copy_with_equality",
        _type_survives_copy_with_equality,
        "Type equality compares identity but Type.copy() makes a new object",
    ),
    (
        "known_instanceof_message_for_type_operand",
        _instanceof_message_does_not_blame_a_valid_right_operand,
        "a Type on the left always reports 'Right operand ... must be a Class or Type'",
    ),
    (
        "known_bare_println_on_its_own_line",
        _bare_println_on_its_own_line,
        "bare PRINTLN is only accepted as the very last token of the file",
    ),
    (
        "known_empty_interpolation",
        _empty_interpolation_is_a_syntax_error,
        "an empty ${} becomes STR() and fails at runtime with an argument-count error",
    ),
    (
        "known_missing_file_outside_root",
        _missing_file_outside_the_root_gives_the_same_error,
        "the existence check runs before the root check, revealing which files exist and leaking a path",
    ),
    (
        "known_null_left_operand_arithmetic",
        _null_on_the_left_is_guarded_like_on_the_right,
        "only a NULL right operand is rejected; NULL + 1 evaluates to 1",
    ),
]
