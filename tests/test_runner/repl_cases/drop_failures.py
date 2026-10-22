"""Dropped file failure checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import (
    PROMPT,
    expect_equal,
    expect_in,
    expect_not_in,
    expect_startswith,
    expect_true,
    make_symlink,
)
from .drop_options import OK_FILE, _drop
from .support import EOF_TAIL


def _dropped_file_runtime_error():
    files = {"err.glad": "LET x = 1 / 0\n"}
    body = _drop(["err.glad -y"], files)
    expect_startswith(
        body, PROMPT + "Running 'err.glad'...\nTraceback", "traceback follows"
    )
    expect_in("err.glad, line 1, in <repl>", body, "location names the file")
    expect_in("Runtime Error: Division by zero", body, "message")
    expect_true(body.endswith(EOF_TAIL), "shell keeps running afterwards")


def _dropped_file_missing():
    expect_equal(
        _drop(["nope.glad"]),
        PROMPT + "Error: File not found: 'nope.glad'\n" + EOF_TAIL,
        "missing file is reported",
    )


def _dropped_file_symlink_denied():
    def setup(directory):
        make_symlink(directory / "link.glad", directory / "ok.glad")

    expect_equal(
        _drop(["link.glad -y"], OK_FILE, setup=setup),
        PROMPT + "Access denied: 'link.glad' is a symbolic link\n" + EOF_TAIL,
        "symbolic links are refused",
    )


def _dropped_file_size_limit():
    limit = Settings.MAX_SOURCE_BYTES
    data = {"big.glad": b"#" + b"x" * (limit - 1) + b"\n"}
    expect_equal(
        _drop(["big.glad -y"], binary_files=data),
        PROMPT
        + f"Error: File too large ({limit + 1:,} bytes). Maximum allowed: {limit:,} bytes.\n"
        + EOF_TAIL,
        "oversized file is refused",
    )


def _dropped_file_invalid_utf8():
    expect_equal(
        _drop(["bad.glad -y"], binary_files={"bad.glad": b'PRINTLN "\xff"\n'}),
        PROMPT
        + "Error: 'bad.glad' is not valid UTF-8. Save the file as UTF-8 and try again.\n"
        + EOF_TAIL,
        "non-UTF-8 file is refused",
    )


def _dropped_file_resets_scope_and_keeps_its_definitions():
    files = {"setx.glad": 'LET fx = 7\nPRINTLN "set"\n'}
    body = _drop(["LET keep = 1", "setx.glad -y", "fx + 0", "keep + 0"], files)
    expect_in("set\n", body, "file ran")
    expect_in(PROMPT + "7\n", body, "names defined by the file are visible afterwards")
    expect_in(
        "Runtime Error: 'keep' is not defined", body, "earlier REPL names are gone"
    )


def _file_name_inside_open_block_is_not_dropped():
    body = _drop(["FUNC f()", "ok.glad", "ENDFUNC"], OK_FILE)
    expect_not_in("Running", body, "file names inside a block are plain text")


def _uppercase_extension_is_not_treated_as_file():
    expect_equal(
        _drop(["ok.GLAD"], OK_FILE),
        PROMPT
        + "Traceback (most recent call last):\n"
        + "  File <stdin>, line 1, in <repl>\n"
        + "Runtime Error: 'ok' is not defined\n"
        + EOF_TAIL,
        "only the exact .glad suffix triggers file mode; anything else is code",
    )
