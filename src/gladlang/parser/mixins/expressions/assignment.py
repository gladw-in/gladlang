"""Parse expressions and handle assignments."""

from gladlang.core.constants import (
    GL_BIT_AND,
    GL_BIT_ANDEQ,
    GL_BIT_OR,
    GL_BIT_OREQ,
    GL_BIT_XOR,
    GL_BIT_XOREQ,
    GL_DIV,
    GL_DIVEQ,
    GL_EQ,
    GL_FLOORDIV,
    GL_FLOORDIVEQ,
    GL_LSHIFT,
    GL_LSHIFTEQ,
    GL_MINUS,
    GL_MINUSEQ,
    GL_MOD,
    GL_MODEQ,
    GL_MUL,
    GL_MULEQ,
    GL_PLUS,
    GL_PLUSEQ,
    GL_POW,
    GL_POWEQ,
    GL_RSHIFT,
    GL_RSHIFTEQ,
)
from gladlang.parser.parse_result import ParseResult

COMPOUND_OPERATOR_FOR_ASSIGN_TOKEN = {
    GL_PLUSEQ: GL_PLUS,
    GL_MINUSEQ: GL_MINUS,
    GL_MULEQ: GL_MUL,
    GL_DIVEQ: GL_DIV,
    GL_POWEQ: GL_POW,
    GL_MODEQ: GL_MOD,
    GL_FLOORDIVEQ: GL_FLOORDIV,
    GL_BIT_ANDEQ: GL_BIT_AND,
    GL_BIT_OREQ: GL_BIT_OR,
    GL_BIT_XOREQ: GL_BIT_XOR,
    GL_LSHIFTEQ: GL_LSHIFT,
    GL_RSHIFTEQ: GL_RSHIFT,
}


class ExpressionsAssignment:
    def expression(self):
        result = ParseResult()
        left_node = result.register(self.ternary_expression())
        if result.error:
            return result

        if self.current_token.type not in (
            GL_EQ,
            GL_PLUSEQ,
            GL_MINUSEQ,
            GL_MULEQ,
            GL_DIVEQ,
            GL_POWEQ,
            GL_MODEQ,
            GL_FLOORDIVEQ,
            GL_BIT_ANDEQ,
            GL_BIT_OREQ,
            GL_BIT_XOREQ,
            GL_LSHIFTEQ,
            GL_RSHIFTEQ,
        ):
            return result.success(left_node)

        operator_token = self.current_token
        result.register_advancement()
        self.advance()
        right_node = result.register(self.expression())
        if result.error:
            return result

        binary_operator_type = COMPOUND_OPERATOR_FOR_ASSIGN_TOKEN.get(
            operator_token.type
        )

        return self._build_assignment_node(
            result, left_node, operator_token, binary_operator_type, right_node
        )
