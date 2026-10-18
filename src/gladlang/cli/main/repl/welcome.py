"""Prints the REPL welcome banner."""

import sys

from gladlang.core.util.settings import Settings


def print_repl_welcome():
    sys.stdout.write(f"Welcome to GladLang (v{Settings.VERSION})\n")
    sys.stdout.write("Type 'exit' or 'quit' to close the shell.\n")
    sys.stdout.write("--------------------------------------------------\n")
