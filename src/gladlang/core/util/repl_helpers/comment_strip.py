"""Strips `#` comments line-by-line from already quote-stripped text."""


def strip_comments(source):
    cleaned_lines = []

    for raw_line in source.split("\n"):
        if "#" in raw_line:
            raw_line = raw_line[: raw_line.index("#")]

        cleaned_lines.append(raw_line)

    return "\n".join(cleaned_lines)
