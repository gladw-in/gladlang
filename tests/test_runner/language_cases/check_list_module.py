"""Check list for module value known issues."""

from .known_issue_checks import (
    MODULE_ISSUE,
    _module_operation_must_not_crash,
)

MODULE_CHECKS = [
    (
        "known_module_missing_member",
        _module_operation_must_not_crash("LET r = m.nothing"),
        MODULE_ISSUE,
    ),
    (
        "known_module_member_assignment",
        _module_operation_must_not_crash("m.PI = 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_new_member",
        _module_operation_must_not_crash("m.fresh = 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_indexing",
        _module_operation_must_not_crash("LET r = m[0]"),
        MODULE_ISSUE,
    ),
    (
        "known_module_equality",
        _module_operation_must_not_crash("LET r = m == m"),
        MODULE_ISSUE,
    ),
    (
        "known_module_inequality",
        _module_operation_must_not_crash("LET r = m != 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_identity",
        _module_operation_must_not_crash("LET r = m IS m"),
        MODULE_ISSUE,
    ),
    (
        "known_module_logical_and",
        _module_operation_must_not_crash("LET r = m AND 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_logical_not",
        _module_operation_must_not_crash("LET r = NOT m"),
        MODULE_ISSUE,
    ),
    (
        "known_module_arithmetic",
        _module_operation_must_not_crash("LET r = m + 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_ordering",
        _module_operation_must_not_crash("LET r = m < 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_call",
        _module_operation_must_not_crash("LET r = m()"),
        MODULE_ISSUE,
    ),
    (
        "known_module_unary_minus",
        _module_operation_must_not_crash("LET r = -m"),
        MODULE_ISSUE,
    ),
    (
        "known_module_slice_copy",
        _module_operation_must_not_crash("LET r = [m][0:1]"),
        MODULE_ISSUE,
    ),
    (
        "known_module_compound_member",
        _module_operation_must_not_crash("m.PI += 1"),
        MODULE_ISSUE,
    ),
    (
        "known_module_instanceof_number_literal",
        _module_operation_must_not_crash("LET r = m INSTANCEOF 3"),
        MODULE_ISSUE,
    ),
]
