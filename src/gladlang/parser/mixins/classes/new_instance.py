"""Parses `NEW ClassName(arguments...)`."""

from gladlang.core.constants import (
    GL_COMMA,
    GL_IDENTIFIER,
    GL_KEYWORD,
    GL_LPAREN,
    GL_RPAREN,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import NewInstanceNode
from gladlang.parser.parse_result import ParseResult


class ParserNewInstance:
    def new_instance(self):
        result = ParseResult()

        if not self.current_token.matches(GL_KEYWORD, "NEW"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'NEW'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_IDENTIFIER:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected class name",
                )
            )

        class_name_token = self.current_token
        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_LPAREN:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '(' after class name for 'NEW'",
                )
            )

        result.register_advancement()
        self.advance()
        arguments = []

        if self.current_token.type != GL_RPAREN:
            arguments.append(result.register(self.expression()))
            if result.error:
                return result

            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()
                arguments.append(result.register(self.expression()))
                if result.error:
                    return result

        if self.current_token.type != GL_RPAREN:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ',' or ')'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(NewInstanceNode(class_name_token, arguments))
