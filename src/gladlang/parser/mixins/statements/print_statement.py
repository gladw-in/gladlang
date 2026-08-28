"""PRINT / PRINTLN statement parsing."""

from gladlang.core.constants import GL_COMMA, GL_EOF, GL_LPAREN, GL_RPAREN
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import PrintNode
from gladlang.parser.parse_result import ParseResult


class StatementsPrint:
    def _parse_print_statement(self):
        result = ParseResult()

        is_println = self.current_token.value == "PRINTLN"
        keyword_position = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_EOF:
            return result.success(
                PrintNode(
                    [],
                    should_newline=is_println,
                    position_start=keyword_position,
                    position_end=keyword_position,
                )
            )

        expressions = []

        if self.current_token.type == GL_LPAREN:
            result.register_advancement()
            self.advance()

            if self.current_token.type != GL_RPAREN:
                first_expression = result.register(self.expression())
                if result.error:
                    return result

                expressions.append(first_expression)

                while self.current_token.type == GL_COMMA:
                    result.register_advancement()
                    self.advance()
                    expressions.append(result.register(self.expression()))
                    if result.error:
                        return result

            if self.current_token.type != GL_RPAREN:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ')'",
                    )
                )

            result.register_advancement()
            self.advance()
        else:
            first_expression = result.register(self.expression())
            if result.error:
                return result

            expressions.append(first_expression)

            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()
                expressions.append(result.register(self.expression()))
                if result.error:
                    return result

        if not expressions:
            return result.success(
                PrintNode(
                    [],
                    should_newline=is_println,
                    position_start=keyword_position,
                    position_end=keyword_position,
                )
            )

        return result.success(PrintNode(expressions, should_newline=is_println))
