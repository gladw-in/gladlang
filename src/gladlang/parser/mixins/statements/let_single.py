"""LET single-variable assignment parsing: LET x = expression and LET x[i] = expression."""

from gladlang.core.constants import GL_EQ, GL_LSQUARE, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ListSetNode, VariableAccessNode, VariableAssignNode


class StatementsLetSingle:
    def _parse_let_single(self, result):
        variable_name = self.current_token
        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_LSQUARE:
            result.register_advancement()
            self.advance()
            index_expression = result.register(self.expression())
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
            if self.current_token.type != GL_EQ:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected '='",
                    )
                )

            result.register_advancement()
            self.advance()
            value_expression = result.register(self.expression())
            if result.error:
                return result

            return result.success(
                ListSetNode(
                    VariableAccessNode(variable_name),
                    index_expression,
                    value_expression,
                )
            )

        elif self.current_token.type == GL_EQ:
            result.register_advancement()
            self.advance()
            expression = result.register(self.expression())
            if result.error:
                return result

            return result.success(
                VariableAssignNode(variable_name, expression, is_declaration=True)
            )
        else:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '=' or '['",
                )
            )
