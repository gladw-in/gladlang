"""Tokenize a REPL line into file path, flags, and arguments."""

import shlex


def tokenize_repl_line(line):
    try:
        tokens = shlex.split(line, posix=False)
    except ValueError:
        tokens = line.split()

    first_token = tokens[0].strip("'\"") if tokens else ""
    remaining_tokens = tokens[1:]

    auto_confirm = any(token.lower() in ("-y", "-yes") for token in remaining_tokens)
    auto_deny = any(token.lower() in ("-n", "-no") for token in remaining_tokens)

    positional_arguments = [
        token for token in remaining_tokens if not token.lower().startswith("-")
    ]

    return first_token, positional_arguments, auto_confirm, auto_deny
