"""LET destructuring-assignment parsing: LET [a, b, c] = expression."""

from gladlang.core.constants import GL_COMMA, GL_EQ, GL_IDENTIFIER, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import MultiVariableAssignNode


class StatementsLetDestructure:
    def _parse_let_destructure(self, result):
        result.register_advancement()
        self.advance()
        variable_names = []
        if self.current_token.type == GL_IDENTIFIER:
            variable_names.append(self.current_token)
            result.register_advancement()
            self.advance()
            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()
                if self.current_token.type == GL_IDENTIFIER:
                    variable_names.append(self.current_token)
                    result.register_advancement()
                    self.advance()
                else:
                    return result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "Expected identifier",
                        )
                    )

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
        expression = result.register(self.expression())
        if result.error:
            return result

        return result.success(
            MultiVariableAssignNode(variable_names, expression, is_declaration=True)
        )
