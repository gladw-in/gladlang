"""Runs the command-line checks."""

from ..cli_support import run_checks
from .basic_checks import (
    _existing_file_without_glad_extension_runs,
    _help_wins_over_extra_arguments,
    _inline_code,
    _inline_multi_statement,
    _script_arguments_feed_input,
    _script_file_relative_and_absolute,
    _unicode_output,
)
from .error_checks import (
    _directory_argument_is_rejected,
    _input_without_data_fails,
    _missing_script_file,
    _output_before_error_is_kept,
    _runtime_error_in_file,
    _runtime_error_inline,
    _syntax_error_inline,
    _uncaught_throw,
)
from .file_checks import _file_size_limit, _invalid_utf8_file, _symlink_is_denied
from .piped_checks import (
    _piped_empty_stdin,
    _piped_invalid_utf8_is_replaced,
    _piped_runtime_error,
    _piped_size_limit,
    _piped_stdin_runs_code,
    _piped_syntax_error,
)
from .support import _help, _version

CLI_CHECKS = [
    ("version_long_flag", _version("--version")),
    ("version_short_flag", _version("-v")),
    ("help_long_flag", _help("--help")),
    ("help_short_flag", _help("-h")),
    ("help_wins_over_extra_arguments", _help_wins_over_extra_arguments),
    ("inline_code", _inline_code),
    ("inline_multi_statement", _inline_multi_statement),
    ("script_file_relative_and_absolute", _script_file_relative_and_absolute),
    (
        "existing_file_without_glad_extension",
        _existing_file_without_glad_extension_runs,
    ),
    ("unicode_output", _unicode_output),
    ("script_arguments_feed_input", _script_arguments_feed_input),
    ("input_without_data_fails", _input_without_data_fails),
    ("runtime_error_in_file", _runtime_error_in_file),
    ("runtime_error_inline", _runtime_error_inline),
    ("syntax_error_inline", _syntax_error_inline),
    ("uncaught_throw", _uncaught_throw),
    ("output_before_error_is_kept", _output_before_error_is_kept),
    ("missing_script_file", _missing_script_file),
    ("directory_argument_is_rejected", _directory_argument_is_rejected),
    ("file_size_limit", _file_size_limit),
    ("invalid_utf8_file", _invalid_utf8_file),
    ("symlink_is_denied", _symlink_is_denied),
    ("piped_stdin_runs_code", _piped_stdin_runs_code),
    ("piped_empty_stdin", _piped_empty_stdin),
    ("piped_runtime_error", _piped_runtime_error),
    ("piped_syntax_error", _piped_syntax_error),
    ("piped_invalid_utf8_is_replaced", _piped_invalid_utf8_is_replaced),
    ("piped_size_limit", _piped_size_limit),
]


def run_cli_cases(passed_count, failed_count, failure_list):
    return run_checks("cli", CLI_CHECKS, passed_count, failed_count, failure_list)
