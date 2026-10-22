"""Check list for REPL sessions."""

from .session_basics import (
    _banner_and_exit_command,
    _comparison_expressions_are_echoed,
    _eof_exits_cleanly,
    _exit_command_variants,
    _expression_results_are_echoed,
    _print_statement_output_is_not_duplicated,
    _state_persists_between_lines,
    _statements_are_not_echoed,
)
from .session_blocks import (
    _backtick_template_spans_lines,
    _blank_lines_and_comments_are_ignored,
    _multiline_block_uses_continuation_prompt,
    _nested_blocks_run_as_one_unit,
    _open_bracket_waits_for_more_input,
    _trailing_comment_does_not_hide_result,
    _triple_quoted_string_spans_lines,
)
from .session_errors import (
    _buffer_limit_clears_buffer,
    _exit_inside_open_block_is_not_a_command,
    _keyboard_interrupt_discards_buffer,
    _memory_error_is_reported_and_recovers,
    _runtime_error_is_reported_and_state_survives,
    _syntax_error_is_reported_and_session_continues,
    _undefined_name_error,
    _unexpected_exception_becomes_shell_error,
)

SESSION_CHECKS = [
    ("banner_and_exit_command", _banner_and_exit_command),
    ("exit_command_variants", _exit_command_variants),
    ("eof_exits_cleanly", _eof_exits_cleanly),
    ("expression_results_are_echoed", _expression_results_are_echoed),
    ("comparison_expressions_are_echoed", _comparison_expressions_are_echoed),
    ("statements_are_not_echoed", _statements_are_not_echoed),
    ("print_output_is_not_duplicated", _print_statement_output_is_not_duplicated),
    ("state_persists_between_lines", _state_persists_between_lines),
    (
        "multiline_block_uses_continuation_prompt",
        _multiline_block_uses_continuation_prompt,
    ),
    ("nested_blocks_run_as_one_unit", _nested_blocks_run_as_one_unit),
    ("open_bracket_waits_for_more_input", _open_bracket_waits_for_more_input),
    ("triple_quoted_string_spans_lines", _triple_quoted_string_spans_lines),
    ("backtick_template_spans_lines", _backtick_template_spans_lines),
    ("blank_lines_and_comments_are_ignored", _blank_lines_and_comments_are_ignored),
    ("trailing_comment_keeps_result", _trailing_comment_does_not_hide_result),
    ("runtime_error_keeps_state", _runtime_error_is_reported_and_state_survives),
    ("syntax_error_session_continues", _syntax_error_is_reported_and_session_continues),
    ("undefined_name_error", _undefined_name_error),
    ("buffer_limit_clears_buffer", _buffer_limit_clears_buffer),
    ("keyboard_interrupt_discards_buffer", _keyboard_interrupt_discards_buffer),
    ("memory_error_recovers", _memory_error_is_reported_and_recovers),
    (
        "unexpected_exception_becomes_shell_error",
        _unexpected_exception_becomes_shell_error,
    ),
    ("exit_inside_open_block", _exit_inside_open_block_is_not_a_command),
]
