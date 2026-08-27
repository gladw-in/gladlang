"""Parse atoms like literals, identifiers, THIS/SUPER, parenthesized expressions, lists, dicts, definitions, and NEW."""

from gladlang.core.constants import (
    GL_FLOAT,
    GL_IDENTIFIER,
    GL_INT,
    GL_KEYWORD,
    GL_LBRACE,
    GL_LPAREN,
    GL_LSQUARE,
    GL_RPAREN,
    GL_STRING,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import NumberNode, StringNode, VariableAccessNode
from gladlang.parser.parse_result import ParseResult


class ExpressionsAtom:
    def atom(self):
        result = ParseResult()
        current_tokenen = self.current_token

        if current_tokenen.type == GL_LBRACE:
            return self.dict_expression()

        if current_tokenen.type in (GL_INT, GL_FLOAT):
            result.register_advancement()
            self.advance()
            return result.success(NumberNode(current_tokenen))
        elif current_tokenen.type == GL_STRING:
            result.register_advancement()
            self.advance()
            return result.success(StringNode(current_tokenen))
        elif current_tokenen.type == GL_IDENTIFIER:
            result.register_advancement()
            self.advance()
            return result.success(VariableAccessNode(current_tokenen))
        elif current_tokenen.matches(GL_KEYWORD, "THIS"):
            result.register_advancement()
            self.advance()
            return result.success(VariableAccessNode(current_tokenen))
        elif current_tokenen.matches(GL_KEYWORD, "SUPER"):
            result.register_advancement()
            self.advance()
            return result.success(VariableAccessNode(current_tokenen))
        elif current_tokenen.type == GL_LPAREN:
            result.register_advancement()
            self.advance()
            expression = result.register(self.expression())
            if result.error:
                return result

            if self.current_token.type == GL_RPAREN:
                result.register_advancement()
                self.advance()
                return result.success(expression)
            else:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ')'",
                    )
                )
        elif current_tokenen.type == GL_LSQUARE:
            return self.list_expression()
        elif current_tokenen.matches(GL_KEYWORD, "DEF"):
            return self.function_definition()
        elif current_tokenen.matches(GL_KEYWORD, "CLASS"):
            return self.class_definition()
        elif current_tokenen.matches(GL_KEYWORD, "NEW"):
            return self.new_instance()

        return result.failure(
            InvalidSyntaxError(
                current_tokenen.position_start,
                current_tokenen.position_end,
                "Expected int, float, string, identifier, '+', '-', '++', '--', '(', '[', 'DEF', 'CLASS', or 'NEW'",
            )
        )
