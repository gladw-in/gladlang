"""Shared constants and helpers for the REPL checks."""

from ..cli_support import PROMPT

EOF_TAIL = PROMPT + "\nExiting.\n"


EXIT_TAIL = PROMPT


def _lines(*texts):
    return list(texts)


def _write(directory, name, text):
    path = directory / name
    path.write_text(text, encoding="utf-8", newline="\n")
    return path
