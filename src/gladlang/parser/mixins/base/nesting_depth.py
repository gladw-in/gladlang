"""Check nesting depth and ternary chains before parsing."""

from gladlang.core.constants import (
    GL_LBRACE,
    GL_LPAREN,
    GL_LSQUARE,
    GL_QMARK,
    GL_RBRACE,
    GL_RPAREN,
    GL_RSQUARE,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.core.util.settings import Settings
from gladlang.parser.parse_result import ParseResult


class ParserNestingDepth:
    def check_nesting_depth(self):
        paren_depth = brace_depth = bracket_depth = 0
        max_paren_depth = max_brace_depth = max_bracket_depth = 0
        ternary_count = 0

        for token in self.tokens:
            if token.type == GL_LPAREN:
                paren_depth += 1
                max_paren_depth = max(max_paren_depth, paren_depth)
            elif token.type == GL_RPAREN:
                paren_depth = max(0, paren_depth - 1)
            elif token.type == GL_LBRACE:
                brace_depth += 1
                max_brace_depth = max(max_brace_depth, brace_depth)
            elif token.type == GL_RBRACE:
                brace_depth = max(0, brace_depth - 1)
            elif token.type == GL_LSQUARE:
                bracket_depth += 1
                max_bracket_depth = max(max_bracket_depth, bracket_depth)
            elif token.type == GL_RSQUARE:
                bracket_depth = max(0, bracket_depth - 1)
            elif token.type == GL_QMARK:
                ternary_count += 1

        worst_depth = max(max_paren_depth, max_brace_depth, max_bracket_depth)
        if worst_depth > Settings.MAX_NESTING:
            first_token = self.tokens[0] if self.tokens else None
            last_token = self.tokens[-1] if self.tokens else None

            return ParseResult().failure(
                InvalidSyntaxError(
                    first_token.position_start if first_token else None,
                    last_token.position_end if last_token else None,
                    f"Expression nesting depth ({worst_depth}) exceeds limit ({Settings.MAX_NESTING})",
                )
            )

        if ternary_count > Settings.MAX_TERNARY_CHAIN:
            first_token = self.tokens[0] if self.tokens else None
            last_token = self.tokens[-1] if self.tokens else None

            return ParseResult().failure(
                InvalidSyntaxError(
                    first_token.position_start if first_token else None,
                    last_token.position_end if last_token else None,
                    f"Too many chained ternary expressions ({ternary_count}) exceeds limit ({Settings.MAX_TERNARY_CHAIN})",
                )
            )

        return None
