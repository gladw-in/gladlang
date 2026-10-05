"""Parse function argument list between parentheses."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_KEYWORD, GL_RPAREN
from gladlang.core.errors import InvalidSyntaxError


class ParserFunctionArguments:
    def _parse_function_arguments(self, result, open_parentheses_position):
        argument_tokens = []

        if self.current_token.type != GL_RPAREN:
            if self.current_token.type == GL_IDENTIFIER:
                if self.current_token.value in [
                    token.value for token in argument_tokens
                ]:
                    result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            f"Duplicate function argument '{self.current_token.value}'",
                        )
                    )
                    return None

                argument_tokens.append(self.current_token)
            elif self.current_token.matches(GL_KEYWORD, "THIS"):
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "'THIS' is reserved and cannot be used as a parameter name",
                    )
                )
                return None
            else:
                result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier",
                    )
                )
                return None

            result.register_advancement()
            self.advance()

            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()

                if self.current_token.type == GL_IDENTIFIER:
                    if self.current_token.value in [
                        token.value for token in argument_tokens
                    ]:
                        result.failure(
                            InvalidSyntaxError(
                                self.current_token.position_start,
                                self.current_token.position_end,
                                f"Duplicate function argument '{self.current_token.value}'",
                            )
                        )
                        return None

                    argument_tokens.append(self.current_token)
                elif self.current_token.matches(GL_KEYWORD, "THIS"):
                    result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "'THIS' is reserved and cannot be used as a parameter name",
                        )
                    )
                    return None
                else:
                    result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "Expected identifier",
                        )
                    )
                    return None

                result.register_advancement()
                self.advance()

        if self.current_token.type != GL_RPAREN:
            result.failure(
                InvalidSyntaxError(
                    open_parentheses_position,
                    self.current_token.position_end,
                    "Expected ',' or ')'",
                )
            )
            return None

        return argument_tokens
