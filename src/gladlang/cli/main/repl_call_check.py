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
                current = source[index]

                if current in '"`':
                    quote = current
                    index += 1

                    while index < length and source[index] != quote:
                        if source[index] == "\\":
                            index += 1

                        index += 1

                    index += 1
                    continue

                if current == character:
                    depth += 1
                elif current == closing:
                    depth -= 1

                index += 1

            if character == "(":
                found_call = True

        elif character == ".":
            index += 1
            member_match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", source[index:])
            if not member_match:
                return False

            index += member_match.end()
        else:
            break

    return found_call and source[index:].strip() == ""
