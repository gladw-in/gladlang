"""Finish parsing a dict comprehension after its first pair."""

from gladlang.core.constants import GL_RBRACE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import DictComprehensionNode


class ParserDictComprehension:
    def _finish_dict_comprehension(self, result, key, value, start_position):
        iteration_specifications = self._parse_comprehension_clauses(result)
        if result.error:
            return result

        if self.current_token.type != GL_RBRACE:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '}'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            DictComprehensionNode(
                key,
                value,
                iteration_specifications,
                start_position,
                self.current_token.position_start.copy(),
            )
        )
