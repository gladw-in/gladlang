"""Remove double-quoted string contents for safe scanning."""


def strip_double_quoted(source):
    cleaned = []
    index = 0
    length = len(source)

    while index < length:
        if source[index] == '"':
            index += 1
            while index < length:
                if source[index] == "\\":
                    index += 2
                elif source[index] == '"':
                    index += 1
                    break
                else:
                    index += 1
        else:
            cleaned.append(source[index])
            index += 1

    return "".join(cleaned)
