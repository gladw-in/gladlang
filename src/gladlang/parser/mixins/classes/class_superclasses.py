"""Parses an optional `INHERITS A, B, ...` clause after the class name."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import VariableAccessNode


class ParserClassSuperclasses:
    def _parse_superclasses(self, result):
        superclasses = []
        if not self.current_token.matches(GL_KEYWORD, "INHERITS"):
            return superclasses

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_IDENTIFIER:
            result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected superclass name",
                )
            )
            return None

        superclasses.append(VariableAccessNode(self.current_token))
        result.register_advancement()
        self.advance()

        while self.current_token.type == GL_COMMA:
            result.register_advancement()
            self.advance()

            if self.current_token.type != GL_IDENTIFIER:
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected superclass name",
                    )
                )
                return None

            superclasses.append(VariableAccessNode(self.current_token))
            result.register_advancement()
            self.advance()

        return superclasses
