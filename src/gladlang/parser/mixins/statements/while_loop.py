"""WHILE loop parsing."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import WhileNode
from gladlang.parser.parse_result import ParseResult


class StatementsWhileLoop:
    def while_expression(self):
        result = ParseResult()
        if not self.current_token.matches(GL_KEYWORD, "WHILE"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'WHILE'",
                )
            )

        result.register_advancement()
        self.advance()
        condition = result.register(self.expression())
        if result.error:
            return result

        self.loop_count += 1
        body = result.register(self.statement_list(("ENDWHILE",)))
        self.loop_count -= 1
        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "ENDWHILE"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDWHILE'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(WhileNode(condition, body))
