"""Iterator-style FOR loop parsing: FOR x IN iterable ... ENDFOR."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ForNode


class StatementsForIterator:
    def _parse_iterator_for(self, result):
        variable_tokens, variable_result = self.parse_iterator_variables()
        if variable_result and variable_result.error:
            return result.failure(variable_result.error)

        if not variable_tokens:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected identifier or '[...]' for loop variable",
                )
            )

        result.advance_count += variable_result.advance_count
        if not self.current_token.matches(GL_KEYWORD, "IN"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'IN'",
                )
            )

        result.register_advancement()
        self.advance()
        iterable_node = result.register(self.expression())
        if result.error:
            return result

        self.loop_count += 1
        body_node = result.register(self.statement_list(("ENDFOR",)))
        self.loop_count -= 1
        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "ENDFOR"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDFOR'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(ForNode(variable_tokens, iterable_node, body_node))
