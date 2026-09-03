"""Top-level entry point: is a REPL input buffer a complete statement yet?"""

from .bracket_balance import brackets_and_keywords_balanced
from .comment_strip import strip_comments
from .quote_stripping import strip_double_quoted
from .unterminated_check import has_unterminated_multiline


def is_complete(source):
    if has_unterminated_multiline(source):
        return False

    if source.count("`") % 2:
        return False

    stripped_text = strip_comments(strip_double_quoted(source))

    if stripped_text.count('"') % 2:
        return False

    return brackets_and_keywords_balanced(stripped_text)
