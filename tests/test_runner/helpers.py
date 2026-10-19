"""Shared helpers for reading files, running sources, and inspecting output."""

import os
import signal
import threading
from contextlib import contextmanager
from pathlib import Path

from gladlang.core.util.runner import run
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.settings import Settings
from gladlang.runtime.context import Context
from gladlang.values.classes.class_ import Class

FAILURE_SUFFIXES = ("(FAIL)", "is wrong", "test failed (0)")
FAILURE_PREFIXES = ("FAIL:", "[FAIL]", "ERROR: Should", "This should NOT")


def read_file_safe(path):
    try:
        O_NOFOLLOW = os.O_NOFOLLOW
        file_descriptor = os.open(str(path), os.O_RDONLY | O_NOFOLLOW)
    except AttributeError:
        file_descriptor = os.open(str(path), os.O_RDONLY)

    try:
        file_size = os.fstat(file_descriptor).st_size
        if file_size > Settings.MAX_SOURCE_BYTES:
            os.close(file_descriptor)
            return (
                None,
                f"File too large: {file_size:,} bytes (max {Settings.MAX_SOURCE_BYTES:,})",
            )

        file_handle = os.fdopen(file_descriptor, "r", encoding="utf-8")

        try:
            return file_handle.read(), None
        except UnicodeDecodeError:
            return None, f"File is not valid UTF-8: {Path(path).name}"
        finally:
            file_handle.close()
    except Exception:
        os.close(file_descriptor)
        raise


def run_source(name, source_code):
    context = Context(f"<regression:{name}>")
    context.symbol_table = get_fresh_global_scope()

    _, error = run(f"<regression:{name}>", source_code, context, instruction_limit=None)
    return error


def has_explicit_test_failure(output):
    for line in output.splitlines():
        line = line.strip()
        if (
            line.startswith(FAILURE_PREFIXES)
            or line.endswith(FAILURE_SUFFIXES)
            or line == "FAIL"
            or line == "RESULT: FAILURE"
        ):
            return True

        if line.startswith("FAILED:"):
            try:
                if int(line.split(":", 1)[1].strip()) > 0:
                    return True
            except ValueError:
                return True

    return False


def check_class_copy_cache_isolation():
    original = Class("CacheTest", [], {})
    original._method_cache["original"] = object()

    copied = original.copy()

    if copied._method_cache is original._method_cache:
        raise AssertionError("Class copy shares its method cache")

    copied._method_cache["copied"] = object()

    if "copied" in original._method_cache:
        raise AssertionError("Copy cache mutation affected original")

    original._method_cache["original_only"] = object()

    if "original_only" in copied._method_cache:
        raise AssertionError("Original cache mutation affected copy")


class TestTimeout(Exception):
    pass


@contextmanager
def time_limit(seconds):
    usable = (
        hasattr(signal, "setitimer")
        and threading.current_thread() is threading.main_thread()
    )

    if not usable:
        yield
        return

    def _raise(signum, frame):
        raise TestTimeout(f"Test exceeded {seconds}s time limit")

    previous = signal.signal(signal.SIGALRM, _raise)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
