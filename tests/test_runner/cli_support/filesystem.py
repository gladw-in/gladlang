"""Temporary directory, working directory, and symlink helpers."""

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .assertions import Skip


@contextmanager
def temporary_directory():
    with tempfile.TemporaryDirectory(prefix="gladlang_cli_") as directory:
        yield Path(directory)


@contextmanager
def working_directory(path):
    previous = os.getcwd()
    os.chdir(str(path))

    try:
        yield
    finally:
        os.chdir(previous)


def make_symlink(link_path, target_path):
    try:
        os.symlink(str(target_path), str(link_path))
    except (OSError, NotImplementedError, AttributeError) as reason:
        raise Skip(f"symbolic links unavailable: {reason}")
