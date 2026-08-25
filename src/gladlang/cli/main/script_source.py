"""Resolve a CLI argument into source code and a source name."""

import os
import sys
from pathlib import Path

from gladlang.core.util.settings import Settings


def resolve_script_source(argument):
    is_file = False
    absolute_path = None

    looks_like_file_reference = argument.endswith(".glad") or os.path.exists(argument)

    if looks_like_file_reference and Path(argument).is_symlink():
        sys.stderr.write(f"Access denied: '{argument}' is a symbolic link\n")
        sys.exit(1)

    if looks_like_file_reference:
        try:
            candidate_path = Path(argument)
            strict_path = candidate_path.resolve(strict=False)

            try:
                O_NOFOLLOW = os.O_NOFOLLOW
                file_descriptor = os.open(str(strict_path), os.O_RDONLY | O_NOFOLLOW)
            except AttributeError:
                file_descriptor = os.open(str(strict_path), os.O_RDONLY)

            file_size = os.fstat(file_descriptor).st_size
            if file_size > Settings.MAX_SOURCE_BYTES:
                os.close(file_descriptor)
                sys.stderr.write(
                    f"File too large: '{argument}' ({file_size:,} bytes). "
                    f"Maximum allowed: {Settings.MAX_SOURCE_BYTES:,} bytes.\n"
                )
                sys.exit(1)

            try:
                with os.fdopen(file_descriptor, "r", encoding="utf-8") as file_handle:
                    source_code = file_handle.read()
            except UnicodeDecodeError:
                sys.stderr.write(
                    f"Encoding error: '{argument}' is not valid UTF-8. "
                    "Save the file as UTF-8 and try again.\n"
                )
                sys.exit(1)

            is_file = True
            absolute_path = candidate_path.resolve()
        except (OSError, PermissionError) as exception:
            sys.stderr.write(f"Error accessing file: {exception}\n")
            sys.exit(1)

    if is_file or argument.endswith(".glad"):
        source_name = str(absolute_path)
        return source_code, source_name

    source_code = argument
    source_name = "<cmdline>"

    if len(source_code.encode("utf-8", errors="replace")) > Settings.MAX_SOURCE_BYTES:
        sys.stderr.write(
            f"Source too large ({len(source_code):,} chars). "
            f"Maximum allowed: {Settings.MAX_SOURCE_BYTES:,} bytes.\n"
        )
        sys.exit(1)

    return source_code, source_name
