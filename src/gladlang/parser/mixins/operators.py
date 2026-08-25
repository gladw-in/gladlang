"""Binary operator helper and bitwise/shift operators."""

from gladlang.core.constants import (
    GL_BIT_OR,
    GL_BIT_XOR,
    GL_BIT_AND,
    GL_LSHIFT,
    GL_RSHIFT,
)
from gladlang.parser.ast import BinaryOperatorNode
from gladlang.parser.parse_result import ParseResult


class ParserOperators:
    def binary_operator(self, function_a, operators, function_b=None):
        if function_b is None:
            function_b = function_a

        result = ParseResult()
        left = result.register(function_a())
        if result.error:
            return result

        while (
            self.current_token.type in operators
            or (self.current_token.type, self.current_token.value) in operators
        ):
            previous_token = self.tokens[self.token_index - 1]
            if (
                self.current_token.position_start.line
                != previous_token.position_end.line
            ):
                break

            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            right = result.register(function_b())
            if result.error:
                return result

            left = BinaryOperatorNode(left, operator_token, right)

        return result.success(left)

    def bitwise_or_expression(self):
        return self.binary_operator(self.bitwise_xor_expression, (GL_BIT_OR,))

    def bitwise_xor_expression(self):
        return self.binary_operator(self.bitwise_and_expression, (GL_BIT_XOR,))

    def bitwise_and_expression(self):
        return self.binary_operator(self.shift_expression, (GL_BIT_AND,))

    def shift_expression(self):
        return self.binary_operator(self.arith_expression, (GL_LSHIFT, GL_RSHIFT))
