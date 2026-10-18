"""Remove double-quoted and backtick string contents for safe scanning."""


def strip_double_quoted(source):
    cleaned_characters = []
    index = 0
    length = len(source)

    while index < length:
        if source[index] in ('"', "`"):
            quote = source[index]
            index += 1
            while index < length:
                if source[index] == "\\":
                    index += 2
                elif source[index] == quote:
                    index += 1
                    break
                else:
                    index += 1
        else:
            cleaned_characters.append(source[index])
            index += 1

    return "".join(cleaned_characters)
