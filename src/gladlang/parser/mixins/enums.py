"""Enum definitions."""

from gladlang.core.constants import (
    GL_KEYWORD,
    GL_IDENTIFIER,
    GL_EQ,
    GL_COMMA,
    GL_EOF,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import EnumNode
from gladlang.parser.parse_result import ParseResult


class ParserEnums:
    def enum_definition(self):
        result = ParseResult()

        if not self.current_token.matches(GL_KEYWORD, "ENUM"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENUM'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_IDENTIFIER:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected enum name",
                )
            )

        enum_name_token = self.current_token
        position_start = enum_name_token.position_start.copy()
        result.register_advancement()
        self.advance()

        cases = []
        while self.current_token.type != GL_EOF and not self.current_token.matches(
            GL_KEYWORD, "ENDENUM"
        ):
            if self.current_token.type != GL_IDENTIFIER:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier or 'ENDENUM'",
                    )
                )

            case_name_token = self.current_token
            result.register_advancement()
            self.advance()

            case_value_node = None
            if self.current_token.type == GL_EQ:
                result.register_advancement()
                self.advance()
                case_value_node = result.register(self.expression())
                if result.error:
                    return result

            cases.append((case_name_token, case_value_node))

            if self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()

        if not self.current_token.matches(GL_KEYWORD, "ENDENUM"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDENUM'",
                )
            )

        position_end = self.current_token.position_end.copy()
        result.register_advancement()
        self.advance()

        return result.success(
            EnumNode(enum_name_token, cases, position_start, position_end)
        )
