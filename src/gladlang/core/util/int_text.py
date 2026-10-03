"""Integer and text conversion – works even when Python's _pylong module is missing."""

from gladlang.core.util.settings import Settings


def int_to_str(value):
    if not isinstance(value, int) or isinstance(value, bool):
        return str(value)

    try:
        return str(value)
    except ModuleNotFoundError:
        pass

    sign = "-" if value < 0 else ""
    remaining = abs(value)

    chunks = []
    while remaining:
        remaining, chunk = divmod(remaining, 10**Settings.INT_TO_STR_CHUNK_DIGITS)
        chunks.append(chunk)

    leading_chunk = chunks.pop()
    parts = [str(leading_chunk)]
    for chunk in reversed(chunks):
        parts.append(str(chunk).zfill(Settings.INT_TO_STR_CHUNK_DIGITS))

    return sign + "".join(parts)


def str_to_int(text, base=10):
    try:
        return int(text, base)
    except ModuleNotFoundError:
        pass

    digits = text.strip()
    sign = 1

    if digits[:1] in ("+", "-"):
        sign = -1 if digits[0] == "-" else 1
        digits = digits[1:]

    if not digits or "_" in digits:
        raise ValueError("invalid literal for integer")

    value = 0
    chunk_size = Settings.INT_TO_STR_CHUNK_DIGITS

    for start in range(0, len(digits), chunk_size):
        chunk = digits[start : start + chunk_size]
        if not chunk.isalnum():
            raise ValueError("invalid literal for integer")

        value = value * base ** len(chunk) + int(chunk, base)

    return sign * value


def int_to_grouped_str(value):
    text = int_to_str(value)
    sign = "-" if text.startswith("-") else ""
    digits = text[len(sign) :]

    first_group_length = len(digits) % 3 or 3
    groups = [digits[:first_group_length]]
    for start in range(first_group_length, len(digits), 3):
        groups.append(digits[start : start + 3])

    return sign + ",".join(groups)
