"""Check if a REPL result should be printed."""

import re
import sys

from .repl_call_check import is_pure_call_expression

STATEMENT_PREFIXES = (
    "LET ",
    "LET[",
    "FINAL ",
    "ENUM ",
    "DEF ",
    "CLASS ",
    "ENDDEF",
    "ENDCLASS",
    "ENDENUM",
    "ENDIF",
    "ENDWHILE",
    "ENDFOR",
    "ENDTRY",
    "ENDSWITCH",
    "IF ",
    "ELSE",
    "WHILE ",
    "FOR ",
    "SWITCH ",
    "TRY",
    "THROW ",
    "RETURN",
    "BREAK",
    "CONTINUE",
    "PRINT",
    "PRINTLN",
    "PUBLIC ",
    "PRIVATE ",
    "PROTECTED ",
    "STATIC ",
    "SUPER",
)


def maybe_print_result(source_text, value):
    lines_without_comments = [
        line for line in source_text.splitlines() if re.sub(r"#.*", "", line).strip()
    ]

    if not lines_without_comments:
        return

    if len(lines_without_comments) != 1:
        return

    stripped_line = re.sub(r"#.*", "", lines_without_comments[0]).strip()

    is_assignment = bool(
        re.match(
            r"^[A-Za-z_][A-Za-z0-9_.]*(\s*\[.+?\])*\s*(\+|-|\*|/|%|\*\*|//|&|\||\^|<<|>>)?=(?!=)",
            stripped_line,
        )
    )

    is_void_call = is_pure_call_expression(stripped_line)

    is_increment = bool(
        re.match(
            r"^(\+\+|--)?[A-Za-z_][A-Za-z0-9_.]*(\s*\[.+?\])*\s*(\+\+|--)?$",
            stripped_line,
        )
    )

    is_statement = any(
        stripped_line.startswith(prefix) for prefix in STATEMENT_PREFIXES
    )

    if not is_statement and not is_assignment and not is_void_call and not is_increment:
        sys.stdout.write(str(value) + "\n")
