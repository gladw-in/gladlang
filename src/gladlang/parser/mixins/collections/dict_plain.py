"""Finish parsing a plain dict literal with key:value pairs."""

from gladlang.core.constants import GL_COLON, GL_COMMA, GL_RBRACE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import DictNode


class ParserDictPlain:
    def _finish_plain_dict(self, result, key, value, start_position):
        key_value_pairs = [(key, value)]

        while self.current_token.type == GL_COMMA:
            result.register_advancement()
            self.advance()

            if self.current_token.type == GL_RBRACE:
                break

            key = result.register(self.expression())
            if result.error:
                return result

            if self.current_token.type != GL_COLON:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ':'",
                    )
                )

            result.register_advancement()
            self.advance()

            value = result.register(self.expression())
            if result.error:
                return result

            key_value_pairs.append((key, value))

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
            DictNode(
                key_value_pairs,
                start_position,
                self.current_token.position_start.copy(),
            )
        )
