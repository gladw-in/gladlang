"""Build assignment AST node for variables, attributes, subscripts, or destructuring."""

from gladlang.core.constants import GL_EQ
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    BinaryOperatorNode,
    GetAttributeNode,
    ListAccessNode,
    ListNode,
    ListSetNode,
    MultiVariableAssignNode,
    SetAttributeNode,
    VariableAccessNode,
    VariableAssignNode,
)
from gladlang.lexer.token import Token


class ExpressionsAssignmentTarget:
    def _build_assignment_node(
        self, result, target_node, operator_token, binary_operator_type, right_node
    ):
        if isinstance(target_node, VariableAccessNode):
            combined_expression = right_node
            if binary_operator_type is not None:
                combined_expression = BinaryOperatorNode(
                    target_node,
                    Token(
                        binary_operator_type,
                        position_start=operator_token.position_start,
                    ),
                    right_node,
                )

            return result.success(
                VariableAssignNode(
                    target_node.variable_name_token,
                    combined_expression,
                    is_declaration=False,
                )
            )
        elif isinstance(target_node, GetAttributeNode):
            return result.success(
                SetAttributeNode(
                    target_node.object_node,
                    target_node.attribute_name_token,
                    right_node,
                    binary_operator_type,
                )
            )
        elif isinstance(target_node, ListAccessNode):
            return result.success(
                ListSetNode(
                    target_node.list_node,
                    target_node.index_node,
                    right_node,
                    binary_operator_type,
                )
            )
        elif (
            isinstance(target_node, ListNode)
            and operator_token.type == GL_EQ
            and target_node.element_nodes
            and all(
                isinstance(element, VariableAccessNode)
                for element in target_node.element_nodes
            )
        ):
            variable_tokens = [
                element.variable_name_token for element in target_node.element_nodes
            ]

            return result.success(
                MultiVariableAssignNode(
                    variable_tokens, right_node, is_declaration=False
                )
            )
        else:
            return result.failure(
                InvalidSyntaxError(
                    target_node.position_start,
                    target_node.position_end,
                    "Invalid assignment target",
                )
            )
