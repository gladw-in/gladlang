"""Script file limit checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import (
    expect_equal,
    expect_in,
    expect_startswith,
    make_symlink,
    run_cli,
    temporary_directory,
)
from .support import _failed, _ok, _write


def _file_size_limit():
    limit = Settings.MAX_SOURCE_BYTES
    with temporary_directory() as directory:
        (directory / "exact.glad").write_bytes(b"#" + b"x" * (limit - 2) + b"\n")
        exact = run_cli(["exact.glad"], cwd=directory)
        _ok(exact, "file of exactly the limit")
        expect_equal(exact.stdout, "", "comment-only file prints nothing")

        (directory / "big.glad").write_bytes(b"#" + b"x" * (limit - 1) + b"\n")
        over = run_cli(["big.glad"], cwd=directory)
        _failed(over, "file over the limit")
        expect_startswith(over.stderr, "File too large: 'big.glad'", "diagnostic")
        expect_in(f"Maximum allowed: {limit:,} bytes.", over.stderr, "limit shown")


def _invalid_utf8_file():
    with temporary_directory() as directory:
        (directory / "bad.glad").write_bytes(b'PRINTLN "\xff\xfe"\n')
        result = run_cli(["bad.glad"], cwd=directory)
        _failed(result, "invalid UTF-8")
        expect_startswith(result.stderr, "Encoding error: 'bad.glad'", "diagnostic")
        expect_in("not valid UTF-8", result.stderr, "reason")


def _symlink_is_denied():
    with temporary_directory() as directory:
        _write(directory, "real.glad", 'PRINTLN "real"\n')
        make_symlink(directory / "link.glad", directory / "real.glad")
        result = run_cli(["link.glad"], cwd=directory)
        _failed(result, "symlink")
        expect_equal(
            result.stderr,
            "Access denied: 'link.glad' is a symbolic link\n",
            "diagnostic",
        )
