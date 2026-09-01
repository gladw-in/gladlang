"""Arithmetic expression parsing: +/- terms, */ /%// factors, unary ops, and power."""

from gladlang.core.constants import (
    GL_BIT_NOT,
    GL_DIV,
    GL_FLOORDIV,
    GL_MINUS,
    GL_MINUSMINUS,
    GL_MOD,
    GL_MUL,
    GL_PLUS,
    GL_PLUSPLUS,
    GL_POW,
)
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    GetAttributeNode,
    ListAccessNode,
    UnaryOperatorNode,
    VariableAccessNode,
)
from gladlang.parser.parse_result import ParseResult


class ExpressionsArithmetic:
    def arith_expression(self):
        return self.binary_operator(self.term, (GL_PLUS, GL_MINUS))

    def term(self):
        return self.binary_operator(self.factor, (GL_MUL, GL_DIV, GL_MOD, GL_FLOORDIV))

    def factor(self):
        result = ParseResult()
        current_tokenen = self.current_token

        if current_tokenen.type in (GL_PLUS, GL_MINUS):
            result.register_advancement()
            self.advance()
            factor_value = result.register(self.factor())
            if result.error:
                return result

            return result.success(UnaryOperatorNode(current_tokenen, factor_value))
        elif current_tokenen.type in (GL_PLUSPLUS, GL_MINUSMINUS):
            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            target_node = result.register(self.call())
            if result.error:
                return result

            if not isinstance(
                target_node, (VariableAccessNode, GetAttributeNode, ListAccessNode)
            ):
                return result.failure(
                    InvalidSyntaxError(
                        target_node.position_start,
                        operator_token.position_end,
                        "Invalid target for pre-increment/decrement operator",
                    )
                )

            return result.success(UnaryOperatorNode(operator_token, target_node))
        elif current_tokenen.type == GL_BIT_NOT:
            result.register_advancement()
            self.advance()
            factor_value = result.register(self.factor())
            if result.error:
                return result

            return result.success(UnaryOperatorNode(current_tokenen, factor_value))

        return self.power()

    def power(self):
        return self.binary_operator(self.call, (GL_POW,), self.factor)
