"""Parse function argument list between parentheses."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_KEYWORD, GL_RPAREN
from gladlang.core.errors import InvalidSyntaxError


class ParserFunctionArguments:
    def _parse_function_arguments(self, result):
        argument_tokens = []

        if self.current_token.type != GL_RPAREN:
            if self.current_token.type == GL_IDENTIFIER:
                argument_tokens.append(self.current_token)
            elif self.current_token.matches(GL_KEYWORD, "THIS"):
                argument_tokens.append(self.current_token)
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
                    argument_tokens.append(self.current_token)
                elif self.current_token.matches(GL_KEYWORD, "THIS"):
                    argument_tokens.append(self.current_token)
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
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ',' or ')'",
                )
            )
            return None

        return argument_tokens
