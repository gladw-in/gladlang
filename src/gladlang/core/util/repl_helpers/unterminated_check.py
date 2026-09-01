"""Detect unterminated triple-quoted or backtick strings in REPL input."""


def has_unterminated_multiline(source):
    index = 0
    in_triple = False
    in_backtick = False

    while index < len(source):
        if not in_triple and not in_backtick and source.startswith('"""', index):
            in_triple = True
            index += 3
            continue

        if in_triple and source.startswith('"""', index):
            in_triple = False
            index += 3
            continue

        if not in_triple and not in_backtick and source[index] == "`":
            in_backtick = True
            index += 1
            continue

        if (
            in_backtick
            and source[index] == "`"
            and (not index or source[index - 1] != "\\")
        ):
            in_backtick = False
            index += 1
            continue

        index += 1

    return in_triple or in_backtick
