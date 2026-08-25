"""Detect and read a dropped .glad file path in the REPL."""

import os
import sys
from pathlib import Path

from gladlang.core.util.settings import Settings

from .repl_dropfile_run import confirm_and_run_dropped_file


def _read_dropped_file(file_path, line):
    resolved_path = file_path.resolve(strict=False)

    try:
        O_NOFOLLOW = os.O_NOFOLLOW
        file_descriptor = os.open(str(resolved_path), os.O_RDONLY | O_NOFOLLOW)
    except AttributeError:
        file_descriptor = os.open(str(resolved_path), os.O_RDONLY)

    file_size = os.fstat(file_descriptor).st_size
    if file_size > Settings.MAX_SOURCE_BYTES:
        os.close(file_descriptor)
        sys.stdout.write(
            f"Error: File too large ({file_size:,} bytes). "
            f"Maximum allowed: {Settings.MAX_SOURCE_BYTES:,} bytes.\n"
        )
        return None

    try:
        with os.fdopen(file_descriptor, "r", encoding="utf-8") as file_handle:
            source = file_handle.read()
    except UnicodeDecodeError:
        sys.stdout.write(
            f"Error: '{line}' is not valid UTF-8. "
            "Save the file as UTF-8 and try again.\n"
        )
        return None

    return source, resolved_path, file_size


def try_handle_dropped_file(
    line, arguments, auto_confirm, auto_deny, full_text, repl_context
):
    if not (not full_text and line.endswith(".glad") and "\n" not in line):
        return False

    file_path = Path(line)

    if file_path.is_symlink():
        sys.stdout.write(f"Access denied: '{line}' is a symbolic link\n")
        return True

    try:
        file_info = _read_dropped_file(file_path, line)
        if file_info is None:
            return True

        source, resolved_path, file_size = file_info

        return confirm_and_run_dropped_file(
            file_path,
            source,
            resolved_path,
            file_size,
            arguments,
            auto_confirm,
            auto_deny,
            repl_context,
        )
    except FileNotFoundError:
        sys.stdout.write(f"Error: File not found: '{line}'\n")
        return True
    except PermissionError as exception:
        sys.stdout.write(f"Error: {exception}\n")
        return True
    except OSError as exception:
        sys.stdout.write(f"Error accessing file: {exception}\n")
        return True
