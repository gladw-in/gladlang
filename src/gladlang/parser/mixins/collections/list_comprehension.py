"""Complete parsing a list comprehension after the FOR clause."""

from gladlang.core.constants import GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ListComprehensionNode


class ParserListComprehension:
    def _finish_list_comprehension(self, result, first_expression, start_position):
        iteration_specifications = self._parse_comprehension_clauses(result)
        if result.error:
            return result

        if self.current_token.type != GL_RSQUARE:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ']'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            ListComprehensionNode(
                first_expression,
                iteration_specifications,
                start_position,
                self.current_token.position_start.copy(),
            )
        )
