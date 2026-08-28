"""Check if a REPL line is a void call to suppress auto-printing."""

import re


def is_pure_call_expression(source):
    match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", source)
    if not match:
        return False

    index = match.end()
    length = len(source)
    found_call = False

    while index < length:
        character = source[index]
        if character in "([":
            closing = ")" if character == "(" else "]"
            depth = 1
            index += 1
            while index < length and depth > 0:
                if source[index] == character:
                    depth += 1
                elif source[index] == closing:
                    depth -= 1

                index += 1

            if character == "(":
                found_call = True

        elif character == ".":
            index += 1
            match2 = re.match(r"[A-Za-z_][A-Za-z0-9_]*", source[index:])
            if not match2:
                return False

            index += match2.end()
        else:
            break

    return found_call and source[index:].strip() == ""
