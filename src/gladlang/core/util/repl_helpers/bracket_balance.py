"""Check if brackets and keywords are balanced in REPL input."""

from .keyword_match import (
    END_KEYS,
    NEUTRAL_KEYS,
    START_KEYS,
    is_identifier_character,
    match_keyword_at,
)


def brackets_and_keywords_balanced(stripped_text):
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    keyword_depth = 0

    index = 0
    length = len(stripped_text)
    while index < length:
        character = stripped_text[index]

        if character == "(":
            paren_depth += 1
            index += 1
            continue
        elif character == ")":
            paren_depth = max(0, paren_depth - 1)
            index += 1
            continue
        elif character == "[":
            bracket_depth += 1
            index += 1
            continue
        elif character == "]":
            bracket_depth = max(0, bracket_depth - 1)
            index += 1
            continue
        elif character == "{":
            brace_depth += 1
            index += 1
            continue
        elif character == "}":
            brace_depth = max(0, brace_depth - 1)
            index += 1
            continue

        inside_comprehension = bracket_depth > 0 or brace_depth > 0

        if not inside_comprehension and stripped_text[index].isalpha():
            matched_keyword = match_keyword_at(
                stripped_text, index, length, NEUTRAL_KEYS
            )
            if matched_keyword:
                after_keyword = index + len(matched_keyword)
                while after_keyword < length and stripped_text[after_keyword] == " ":
                    after_keyword += 1
                if (
                    matched_keyword == "ELSE"
                    and stripped_text.startswith("IF", after_keyword)
                    and (
                        after_keyword + 2 == length
                        or not is_identifier_character(stripped_text[after_keyword + 2])
                    )
                ):
                    index = after_keyword + 2
                else:
                    index = after_keyword
                continue

            matched_keyword = match_keyword_at(stripped_text, index, length, END_KEYS)
            if matched_keyword:
                keyword_depth -= 1
                index += len(matched_keyword)
                continue

            matched_keyword = match_keyword_at(stripped_text, index, length, START_KEYS)
            if matched_keyword:
                keyword_depth += 1
                index += len(matched_keyword)
                continue

        index += 1

    return (
        not paren_depth and not bracket_depth and not brace_depth and keyword_depth <= 0
    )
