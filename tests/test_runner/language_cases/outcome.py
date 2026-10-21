"""Helpers that run GladLang source and capture the result."""

import io
import sys
from contextlib import contextmanager

from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.runner import run
from gladlang.runtime.context import Context


class Outcome:
    def __init__(self, stdout, error, python_exception):
        self.stdout = stdout
        self.error = error
        self.python_exception = python_exception

    @property
    def first_line(self):
        return self.error.splitlines()[0] if self.error else None

    def describe(self):
        return (
            f"stdout={self.stdout!r} error={self.error!r} "
            f"python_exception={self.python_exception!r}"
        )


def evaluate(source, entry_path="<test>"):
    context = Context("<test>")
    context.symbol_table = get_fresh_global_scope()
    captured = io.StringIO()
    original = sys.stdout
    sys.stdout = captured
    error_text = None
    python_exception = None

    try:
        _, error = run(str(entry_path), source, context, instruction_limit=None)
        if error is not None:
            error_text = error.as_string()

    except Exception as exception:
        python_exception = f"{type(exception).__name__}: {exception}"
    finally:
        sys.stdout = original

    return Outcome(
        captured.getvalue().replace("\r\n", "\n"), error_text, python_exception
    )


@contextmanager
def patched(target, **attributes):
    sentinel = object()
    saved = {name: getattr(target, name, sentinel) for name in attributes}
    for name, value in attributes.items():
        setattr(target, name, value)

    try:
        yield
    finally:
        for name, value in saved.items():
            if value is sentinel:
                delattr(target, name)
            else:
                setattr(target, name, value)
