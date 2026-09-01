"""Parses FOR clauses for list/dict comprehensions."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError


class ParserComprehensionClauses:
    def _parse_comprehension_clauses(self, result):
        iteration_specifications = []

        while self.current_token.matches(GL_KEYWORD, "FOR"):
            result.register_advancement()
            self.advance()

            var_name_tokens, variable_result = self.parse_iterator_variables()
            if variable_result and variable_result.error:
                result.failure(variable_result.error)
                return None

            if not var_name_tokens:
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier or '[...]'",
                    )
                )
                return None

            result.advance_count += variable_result.advance_count

            if not self.current_token.matches(GL_KEYWORD, "IN"):
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected 'IN'",
                    )
                )
                return None

            result.register_advancement()
            self.advance()

            iterable = result.register(self.expression())
            if result.error:
                return None

            condition_node = None
            if self.current_token.matches(GL_KEYWORD, "IF"):
                result.register_advancement()
                self.advance()
                condition_node = result.register(self.expression())
                if result.error:
                    return None

            iteration_specifications.append((var_name_tokens, iterable, condition_node))

        return iteration_specifications
