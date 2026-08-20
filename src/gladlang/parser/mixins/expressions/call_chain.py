"""Parse call chains with calls, attributes, subscripts, and postfix operators."""

from gladlang.core.constants import (
    GL_DOT,
    GL_LPAREN,
    GL_LSQUARE,
    GL_MINUSMINUS,
    GL_PLUSPLUS,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    GetAttributeNode,
    ListAccessNode,
    PostOperatorNode,
    VariableAccessNode,
)
from gladlang.parser.parse_result import ParseResult


class ExpressionsCallChain:
    def call(self):
        result = ParseResult()
        current_node = result.register(self.atom())
        if result.error:
            return result

        while True:
            previous_token = self.tokens[self.token_index - 1]
            if (
                self.current_token.position_start.line
                != previous_token.position_end.line
                and (self.current_token.type in (GL_LPAREN, GL_DOT, GL_LSQUARE))
            ):
                break

            if self.current_token.type == GL_LPAREN:
                current_node = result.register(self._parse_call_arguments(current_node))
            elif self.current_token.type == GL_DOT:
                current_node = result.register(
                    self._parse_attribute_access(current_node)
                )
            elif self.current_token.type == GL_LSQUARE:
                current_node = result.register(
                    self._parse_subscript_access(current_node)
                )
            else:
                break

            if result.error:
                return result

        return self.parse_postfix_operator(result, current_node)

    def parse_postfix_operator(self, result, current_node):
        previous_token = self.tokens[self.token_index - 1]
        if (
            self.current_token.type in (GL_PLUSPLUS, GL_MINUSMINUS)
            and self.current_token.position_start.line
            == previous_token.position_end.line
        ):
            if not isinstance(
                current_node, (VariableAccessNode, GetAttributeNode, ListAccessNode)
            ):
                return result.failure(
                    InvalidSyntaxError(
                        current_node.position_start,
                        self.current_token.position_end,
                        "Invalid target for post-increment/decrement operator",
                    )
                )

            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            current_node = PostOperatorNode(current_node, operator_token)

        return result.success(current_node)
