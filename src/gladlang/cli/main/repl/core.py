"""The interactive GladLang shell loop."""

import sys

from gladlang.core.util.settings import Settings
from gladlang.core.util.repl_helpers import is_complete

from .welcome import print_repl_welcome
from .setup_context import make_repl_context
from .evaluate import evaluate_complete_buffer
from ..repl_dropfile import try_handle_dropped_file
from ..repl_tokenize import tokenize_repl_line


def run_repl():
    print_repl_welcome()

    repl_context = make_repl_context()

    buffer = ""

    while True:
        try:
            prompt = "GladLang > " if not buffer else "...        > "
            sys.stdout.write(prompt)
            sys.stdout.flush()

            input_line = sys.stdin.readline()
            if not input_line:
                raise EOFError

            input_line = input_line.rstrip("\n")

            if not buffer and input_line.strip().lower() in ("exit", "quit"):
                break

            (
                first_token,
                positional_arguments,
                auto_confirm,
                auto_deny,
            ) = tokenize_repl_line(input_line.strip())

            if try_handle_dropped_file(
                first_token,
                positional_arguments,
                auto_confirm,
                auto_deny,
                buffer,
                repl_context,
            ):
                continue

            buffer += input_line + "\n"

            if len(buffer) > Settings.MAX_REPL_BUFFER:
                sys.stdout.write(
                    "Error: Input buffer limit exceeded. Clearing buffer.\n"
                )
                buffer = ""
                continue

            if is_complete(buffer):
                if buffer.strip() == "":
                    buffer = ""
                    continue

                evaluate_complete_buffer(buffer, repl_context)

                buffer = ""

        except KeyboardInterrupt:
            sys.stdout.write("\nKeyboardInterrupt\n")
            buffer = ""
            continue
        except MemoryError:
            sys.stdout.write("System Error: Memory Limit Exceeded\n")
            buffer = ""
        except EOFError:
            sys.stdout.write("\nExiting.\n")
            break
        except Exception as exception:
            sys.stdout.write(f"Shell Error: {exception}\n")
            buffer = ""
