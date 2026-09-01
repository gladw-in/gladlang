"""BREAK and CONTINUE statement parsing."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import BreakNode, ContinueNode
from gladlang.parser.parse_result import ParseResult


class StatementsBreakContinue:
    def _parse_break_statement(self):
        result = ParseResult()
        if not self.loop_count:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "'BREAK' outside of loop",
                )
            )
        start_position = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        return result.success(
            BreakNode(start_position, self.current_token.position_start.copy())
        )

    def _parse_continue_statement(self):
        result = ParseResult()
        if not self.loop_count:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "'CONTINUE' outside of loop",
                )
            )

        start_position = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()
        return result.success(
            ContinueNode(start_position, self.current_token.position_start.copy())
        )
