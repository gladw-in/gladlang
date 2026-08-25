"""The interactive GladLang shell: prompt/read/eval loop with multiline buffering."""

import sys

from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.settings import Settings
from gladlang.core.util.repl_helpers import is_complete
from gladlang.core.util.runner import run
from gladlang.runtime.context import Context

from .repl_autoprint import maybe_print_result
from .repl_dropfile import try_handle_dropped_file
from .repl_tokenize import tokenize_repl_line


def run_repl():
    sys.stdout.write(f"Welcome to GladLang (v{Settings.VERSION})\n")
    sys.stdout.write("Type 'exit' or 'quit' to close the shell.\n")
    sys.stdout.write("--------------------------------------------------\n")

    repl_context = Context("<repl>")
    repl_context.symbol_table = get_fresh_global_scope()

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

                result, error = run(
                    "<stdin>",
                    buffer,
                    repl_context,
                    instruction_limit=Settings.MAX_INSTRUCTIONS,
                )

                if error:
                    sys.stdout.write(error.as_string() + "\n")
                elif result is not None:
                    maybe_print_result(buffer, result)

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
