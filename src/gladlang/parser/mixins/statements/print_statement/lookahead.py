"""Lookahead helper for finding a top-level comma in a call."""

from gladlang.core.constants import (
    GL_COMMA,
    GL_EOF,
    GL_LBRACE,
    GL_LPAREN,
    GL_LSQUARE,
    GL_RBRACE,
    GL_RPAREN,
    GL_RSQUARE,
)


class StatementsPrintLookahead:
    def _next_call_has_top_level_comma(self):
        depth = 0

        for index in range(self.token_index + 1, len(self.tokens)):
            token = self.tokens[index]

            if token.type == GL_EOF:
                return False

            if depth == 0 and token.type == GL_COMMA:
                return True

            if depth == 0 and token.type == GL_RPAREN:
                return index == self.token_index + 1

            if token.type in (GL_LPAREN, GL_LSQUARE, GL_LBRACE):
                depth += 1
            elif token.type in (GL_RPAREN, GL_RSQUARE, GL_RBRACE):
                depth -= 1

        return False
