"""Block keyword sets and matcher for balance scanning."""

START_KEYS = {"DEF", "CLASS", "ENUM", "IF", "WHILE", "FOR", "TRY", "SWITCH"}

END_KEYS = {
    "ENDDEF",
    "ENDCLASS",
    "ENDENUM",
    "ENDIF",
    "ENDWHILE",
    "ENDFOR",
    "ENDTRY",
    "ENDSWITCH",
}

NEUTRAL_KEYS = {"ELSE", "CATCH", "FINALLY"}


def is_identifier_character(character):
    return character.isalnum() or character == "_"


def match_keyword_at(text, index, length, keywords):
    for keyword in keywords:
        if (
            (not index or not is_identifier_character(text[index - 1]))
            and text.startswith(keyword, index)
            and (
                index + len(keyword) == length
                or not is_identifier_character(text[index + len(keyword)])
            )
        ):
            return keyword

    return None
