"""Source file reading checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import (
    expect_equal,
    expect_in,
    expect_startswith,
    make_symlink,
    temporary_directory,
)
from .module_path_checks import _module_layout


def _read_source(path):
    from gladlang.runtime.modules.file_access import read_module_source

    result = read_module_source(str(path), None, None, None)
    return (result.error.details if result.error else None), (
        None if result.error else result.value
    )


def _file_access_reads_text():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        expect_equal(
            _read_source(root / "ok.glad"), (None, "PRINTLN 1\n"), "plain read"
        )


def _file_access_rejects_missing_and_directories():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        for target in (root / "nope.glad", root / "sub"):
            message = _read_source(target)[0]
            expect_startswith(
                message, "Module not found: ", f"{target.name} is not a readable file"
            )


def _file_access_refuses_symlinks():
    with temporary_directory() as directory:
        root = _module_layout(directory)
        make_symlink(root / "link.glad", root / "ok.glad")
        message = _read_source(root / "link.glad")[0]
        expect_startswith(message, "Access denied: ", "symlink")
        expect_in("is a symbolic link", message, "reason")


def _file_access_enforces_the_size_limit():
    limit = Settings.MAX_SOURCE_BYTES
    with temporary_directory() as directory:
        exact = directory / "exact.glad"
        exact.write_bytes(b"#" * limit)
        expect_equal(
            _read_source(exact)[0], None, "a file of exactly the limit is read"
        )
        over = directory / "over.glad"
        over.write_bytes(b"#" * (limit + 1))
        message = _read_source(over)[0]
        expect_startswith(message, "Module too large: ", "one byte over the limit")
        expect_in(
            f"({limit + 1:,} bytes, maximum {limit:,})", message, "sizes are reported"
        )


def _file_access_rejects_invalid_utf8():
    with temporary_directory() as directory:
        bad = directory / "bad.glad"
        bad.write_bytes(b"\xff\xfe")
        message = _read_source(bad)[0]
        expect_startswith(message, "Module is not valid UTF-8: ", "invalid bytes")
