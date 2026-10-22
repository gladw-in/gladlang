"""Check list for REPL helpers."""

from .autoprint_checks import (
    _autoprint_ignores_multi_line_input,
    _autoprint_prints_expressions,
    _autoprint_suppresses_statements,
    _autoprint_uses_str_of_value,
)
from .completion_checks import (
    _is_complete_cases,
    _strip_helpers,
    _unterminated_multiline_detection,
)
from .echo_checks import (
    BARE_NAME_ISSUE,
    _bare_variable_is_echoed,
    _indexing_is_echoed,
    _member_access_is_echoed,
    _value_returning_call_is_echoed,
)
from .session_errors import _syntax_error_points_at_the_typed_line
from .terminal_title_checks import _terminal_title

HELPER_CHECKS = [
    ("autoprint_prints_expressions", _autoprint_prints_expressions),
    ("autoprint_suppresses_statements", _autoprint_suppresses_statements),
    ("autoprint_ignores_multi_line_input", _autoprint_ignores_multi_line_input),
    ("autoprint_uses_str_of_value", _autoprint_uses_str_of_value),
    ("strip_helpers", _strip_helpers),
    ("unterminated_multiline_detection", _unterminated_multiline_detection),
    ("is_complete_cases", _is_complete_cases),
    ("terminal_title", _terminal_title),
    (
        "syntax_error_points_at_the_typed_line",
        _syntax_error_points_at_the_typed_line,
        "REPL input always ends with a newline, so end-of-input errors report the next line",
    ),
    ("bare_variable_is_echoed", _bare_variable_is_echoed, BARE_NAME_ISSUE),
    ("indexing_is_echoed", _indexing_is_echoed, BARE_NAME_ISSUE),
    ("member_access_is_echoed", _member_access_is_echoed, BARE_NAME_ISSUE),
    (
        "value_returning_call_is_echoed",
        _value_returning_call_is_echoed,
        "every call is treated as void in repl_call_check.py, so returned values are hidden",
    ),
]
