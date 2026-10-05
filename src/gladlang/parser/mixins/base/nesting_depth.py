"""Check nesting depth and ternary chains before parsing."""

from gladlang.core.constants import (
    GL_COLON,
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
        ternary_stack = []
        max_chain_len = 0
        pending_chain_len = 0
        last_token_end_line = None

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

            token_line = token.position_start.line if token.position_start else None

            if (
                pending_chain_len
                and last_token_end_line is not None
                and token_line is not None
                and token_line != last_token_end_line
            ):
                pending_chain_len = 0

            if token.type == GL_QMARK:
                this_chain_len = pending_chain_len + 1 if pending_chain_len else 1

                ternary_stack.append(
                    {
                        "depth": (paren_depth, brace_depth, bracket_depth),
                        "chain_len": this_chain_len,
                    }
                )

                max_chain_len = max(max_chain_len, this_chain_len)

                pending_chain_len = 0

            elif (
                token.type == GL_COLON
                and ternary_stack
                and ternary_stack[-1]["depth"]
                == (paren_depth, brace_depth, bracket_depth)
            ):
                pending_chain_len = ternary_stack.pop()["chain_len"]

            if token_line is not None:
                last_token_end_line = (
                    token.position_end.line if token.position_end else token_line
                )

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

        if max_chain_len > Settings.MAX_TERNARY_CHAIN:
            first_token = self.tokens[0] if self.tokens else None
            last_token = self.tokens[-1] if self.tokens else None

            return ParseResult().failure(
                InvalidSyntaxError(
                    first_token.position_start if first_token else None,
                    last_token.position_end if last_token else None,
                    f"Too many chained ternary expressions ({max_chain_len}) exceeds limit ({Settings.MAX_TERNARY_CHAIN})",
                )
            )

        return None
