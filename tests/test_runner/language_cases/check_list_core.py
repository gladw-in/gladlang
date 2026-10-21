"""Check list for syntax, paths, files, imports, and memory."""

from .file_access_checks import (
    _file_access_enforces_the_size_limit,
    _file_access_reads_text,
    _file_access_refuses_symlinks,
    _file_access_rejects_invalid_utf8,
    _file_access_rejects_missing_and_directories,
)
from .import_depth_checks import _import_chain_within_the_limit, _import_depth_limit
from .known_issue_checks import _huge_integer_with_float
from .literal_checks import (
    _integer_literal_at_the_limit_is_accepted,
    _integer_literal_limits,
    _syntax_check,
)
from .memory_checks import (
    _memory_limit_failure_is_a_warning,
    _memory_limit_is_skipped_without_the_resource_module,
    _memory_limit_never_exceeds_the_hard_limit,
    _memory_limit_uses_the_requested_size,
)
from .module_path_checks import (
    _path_blocks_symlink_escape,
    _path_rejects_absolute_paths,
    _path_rejects_bad_strings,
    _path_reports_missing_files,
    _path_requires_glad_extension,
    _path_resolves_relative_to_the_importing_file,
    _path_stays_inside_the_root,
)
from .syntax_cases import SYNTAX_CASES

SYNTAX_CHECKS = [
    (f"syntax_{name}", _syntax_check(source, message))
    for name, source, message in SYNTAX_CASES
]


CORE_CHECKS = [
    ("integer_literal_limits", _integer_literal_limits),
    ("long_integer_literal_is_accepted", _integer_literal_at_the_limit_is_accepted),
    ("float_of_huge_integer", _huge_integer_with_float("FLOAT(b)")),
    ("integer_plus_float_overflow", _huge_integer_with_float("b + 1.5")),
    ("integer_minus_float_overflow", _huge_integer_with_float("b - 1.5")),
    ("integer_times_float_overflow", _huge_integer_with_float("b * 1.5")),
    ("float_plus_integer_overflow", _huge_integer_with_float("1.5 + b")),
    ("float_minus_integer_overflow", _huge_integer_with_float("1.5 - b")),
    ("float_times_integer_overflow", _huge_integer_with_float("1.5 * b")),
    ("path_rejects_bad_strings", _path_rejects_bad_strings),
    ("path_rejects_absolute_paths", _path_rejects_absolute_paths),
    ("path_requires_glad_extension", _path_requires_glad_extension),
    ("path_reports_missing_files", _path_reports_missing_files),
    ("path_stays_inside_the_root", _path_stays_inside_the_root),
    (
        "path_resolves_relative_to_importer",
        _path_resolves_relative_to_the_importing_file,
    ),
    ("path_blocks_symlink_escape", _path_blocks_symlink_escape),
    ("file_access_reads_text", _file_access_reads_text),
    (
        "file_access_missing_and_directories",
        _file_access_rejects_missing_and_directories,
    ),
    ("file_access_refuses_symlinks", _file_access_refuses_symlinks),
    ("file_access_size_limit", _file_access_enforces_the_size_limit),
    ("file_access_invalid_utf8", _file_access_rejects_invalid_utf8),
    ("import_depth_limit", _import_depth_limit),
    ("import_chain_within_the_limit", _import_chain_within_the_limit),
    ("memory_limit_uses_requested_size", _memory_limit_uses_the_requested_size),
    ("memory_limit_capped_by_hard_limit", _memory_limit_never_exceeds_the_hard_limit),
    ("memory_limit_failure_is_a_warning", _memory_limit_failure_is_a_warning),
    (
        "memory_limit_skipped_without_resource",
        _memory_limit_is_skipped_without_the_resource_module,
    ),
]
