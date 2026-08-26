"""RETURN and THROW statement parsing."""

from gladlang.core.constants import GL_EOF, GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ReturnNode, ThrowNode, VariableAccessNode
from gladlang.lexer.token import Token
from gladlang.parser.parse_result import ParseResult


class StatementsReturnThrow:
    def _parse_return_statement(self):
        result = ParseResult()
        if not self.function_count:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "'RETURN' outside of function",
                )
            )

        result.register_advancement()
        self.advance()
        start_position = self.current_token.position_start.copy()

        END_KEYWORDS = {
            "ENDDEF",
            "ELSE",
            "ENDIF",
            "ENDWHILE",
            "ENDFOR",
            "ENDTRY",
            "ENDSWITCH",
            "ENDCLASS",
            "CATCH",
            "FINALLY",
            "CASE",
            "DEFAULT",
        }

        if self.current_token.type == GL_EOF or (
            self.current_token.type == GL_KEYWORD
            and self.current_token.value in END_KEYWORDS
        ):
            null_token = Token(GL_IDENTIFIER, "NULL", start_position, start_position)
            null_node = VariableAccessNode(null_token)
            return result.success(ReturnNode(null_node, start_position, start_position))

        expression = result.register(self.expression())
        if result.error:
            return result

        return result.success(
            ReturnNode(expression, start_position, expression.position_end)
        )

    def _parse_throw_statement(self):
        result = ParseResult()
        throw_start = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        expression = result.register(self.expression())
        if result.error:
            return result

        return result.success(
            ThrowNode(expression, throw_start, expression.position_end)
        )
