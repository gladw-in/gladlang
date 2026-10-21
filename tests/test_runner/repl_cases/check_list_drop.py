"""Check list for dropped files and processes."""

from .drop_failures import (
    _dropped_file_invalid_utf8,
    _dropped_file_missing,
    _dropped_file_resets_scope_and_keeps_its_definitions,
    _dropped_file_runtime_error,
    _dropped_file_size_limit,
    _dropped_file_symlink_denied,
    _file_name_inside_open_block_is_not_dropped,
    _uppercase_extension_is_not_treated_as_file,
)
from .drop_options import (
    _dropped_file_arguments_feed_input,
    _dropped_file_auto_confirm,
    _dropped_file_auto_deny,
    _dropped_file_confirmation_declined,
    _dropped_file_confirmation_yes,
    _dropped_file_deny_beats_confirm,
    _dropped_file_flags_are_case_insensitive_and_long,
    _dropped_file_quoted_path,
)
from .import_pipe_checks import (
    _repl_import_may_rebind_a_variable,
    _repl_import_over_constant_is_refused,
    _repl_over_a_real_pipe,
    _repl_started_by_main_on_a_terminal,
)
from .tokenize_checks import _pure_call_detection, _tokenize_cases

DROP_CHECKS = [
    ("dropfile_auto_confirm", _dropped_file_auto_confirm),
    ("dropfile_flag_spellings", _dropped_file_flags_are_case_insensitive_and_long),
    ("dropfile_confirmation_yes", _dropped_file_confirmation_yes),
    ("dropfile_confirmation_declined", _dropped_file_confirmation_declined),
    ("dropfile_auto_deny", _dropped_file_auto_deny),
    ("dropfile_deny_beats_confirm", _dropped_file_deny_beats_confirm),
    ("dropfile_quoted_path", _dropped_file_quoted_path),
    ("dropfile_arguments_feed_input", _dropped_file_arguments_feed_input),
    ("dropfile_runtime_error", _dropped_file_runtime_error),
    ("dropfile_missing", _dropped_file_missing),
    ("dropfile_symlink_denied", _dropped_file_symlink_denied),
    ("dropfile_size_limit", _dropped_file_size_limit),
    ("dropfile_invalid_utf8", _dropped_file_invalid_utf8),
    ("dropfile_resets_scope", _dropped_file_resets_scope_and_keeps_its_definitions),
    ("dropfile_ignored_inside_block", _file_name_inside_open_block_is_not_dropped),
    ("dropfile_uppercase_extension", _uppercase_extension_is_not_treated_as_file),
    ("import_over_constant_is_refused", _repl_import_over_constant_is_refused),
    ("import_may_rebind_a_variable", _repl_import_may_rebind_a_variable),
    ("repl_over_a_real_pipe", _repl_over_a_real_pipe),
    ("repl_started_by_main_on_terminal", _repl_started_by_main_on_a_terminal),
    ("tokenize_repl_line", _tokenize_cases),
    ("pure_call_detection", _pure_call_detection),
]
