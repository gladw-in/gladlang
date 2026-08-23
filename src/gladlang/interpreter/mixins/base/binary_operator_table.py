"""Builds the binary-operator token -> Value-method dispatch table."""

from gladlang.core.constants import (
    GL_PLUS,
    GL_MINUS,
    GL_MUL,
    GL_DIV,
    GL_MOD,
    GL_FLOORDIV,
    GL_POW,
    GL_EE,
    GL_NE,
    GL_LT,
    GL_GT,
    GL_LTE,
    GL_GTE,
    GL_BIT_AND,
    GL_BIT_OR,
    GL_BIT_XOR,
    GL_LSHIFT,
    GL_RSHIFT,
)


class InterpreterBinaryOperatorTable:
    def _build_binary_operator_dispatch(self):
        return {
            GL_PLUS: lambda left_value, right_value: left_value.added_to(right_value),
            GL_MINUS: lambda left_value, right_value: left_value.subbed_by(right_value),
            GL_MUL: lambda left_value, right_value: left_value.multed_by(right_value),
            GL_DIV: lambda left_value, right_value: left_value.dived_by(right_value),
            GL_MOD: lambda left_value, right_value: left_value.modded_by(right_value),
            GL_FLOORDIV: lambda left_value, right_value: left_value.floordived_by(
                right_value
            ),
            GL_POW: lambda left_value, right_value: left_value.powed_by(right_value),
            GL_EE: lambda left_value, right_value: left_value.get_comparison_eq(
                right_value
            ),
            GL_NE: lambda left_value, right_value: left_value.get_comparison_ne(
                right_value
            ),
            GL_LT: lambda left_value, right_value: left_value.get_comparison_lt(
                right_value
            ),
            GL_GT: lambda left_value, right_value: left_value.get_comparison_gt(
                right_value
            ),
            GL_LTE: lambda left_value, right_value: left_value.get_comparison_lte(
                right_value
            ),
            GL_GTE: lambda left_value, right_value: left_value.get_comparison_gte(
                right_value
            ),
            GL_BIT_AND: lambda left_value, right_value: left_value.bitted_and_by(
                right_value
            ),
            GL_BIT_OR: lambda left_value, right_value: left_value.bitted_or_by(
                right_value
            ),
            GL_BIT_XOR: lambda left_value, right_value: left_value.bitted_xor_by(
                right_value
            ),
            GL_LSHIFT: lambda left_value, right_value: left_value.lshifted_by(
                right_value
            ),
            GL_RSHIFT: lambda left_value, right_value: left_value.rshifted_by(
                right_value
            ),
        }
