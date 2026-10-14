"""Import chain depth checks."""

from gladlang.core.util.settings import Settings

from ..cli_support import expect_equal, expect_in, expect_true, temporary_directory
from .outcome import evaluate


def _write_module_chain(directory, length):
    for index in range(length):
        lines = []
        if index < length - 1:
            lines.append(f'IMPORT x AS next_value FROM "./m{index + 1}.glad"')

        lines.append(f"EXPORT LET x = {index}")
        (directory / f"m{index}.glad").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )


def _import_depth_limit():
    depth = Settings.MAX_IMPORT_DEPTH
    with temporary_directory() as directory:
        _write_module_chain(directory, depth)
        at_limit = evaluate(
            'IMPORT x FROM "./m0.glad"\nPRINTLN x', entry_path=directory / "entry.glad"
        )
        expect_equal(
            (at_limit.stdout, at_limit.error),
            ("0\n", None),
            "a chain of exactly the limit loads",
        )

    with temporary_directory() as directory:
        _write_module_chain(directory, depth + 1)
        over = evaluate(
            'IMPORT x FROM "./m0.glad"', entry_path=directory / "entry.glad"
        )
        expect_true(over.python_exception is None, f"no crash: {over.describe()}")
        expect_in(
            f"Maximum import depth exceeded ({depth})",
            over.error or "",
            "one past the limit",
        )


def _import_chain_within_the_limit():
    with temporary_directory() as directory:
        for index in range(5):
            lines = []
            if index < 4:
                lines.append(f'IMPORT x AS next_value FROM "./m{index + 1}.glad"')

            lines.append(f"EXPORT LET x = {index}")
            (directory / f"m{index}.glad").write_text(
                "\n".join(lines) + "\n", encoding="utf-8"
            )
        outcome = evaluate(
            'IMPORT x FROM "./m0.glad"\nPRINTLN x', entry_path=directory / "entry.glad"
        )
        expect_equal(
            (outcome.stdout, outcome.error), ("0\n", None), "a short chain loads"
        )
