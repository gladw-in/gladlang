"""Parse static field declarations inside a class body."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    FinalVariableAssignNode,
    VariableAssignNode,
    VisibilityStatementNode,
)


class ParserClassField:
    def _parse_class_field(self, result, visibility, is_static, static_fields):
        is_final_declaration = self.current_token.matches(GL_KEYWORD, "FINAL")
        if is_final_declaration and not is_static:
            result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Class-level constants must be declared with STATIC FINAL",
                )
            )
            return False

        assign_node = result.register(self.statement())
        if result.error:
            return False

        if not isinstance(
            assign_node,
            (VariableAssignNode, FinalVariableAssignNode, VisibilityStatementNode),
        ):
            result.failure(
                InvalidSyntaxError(
                    assign_node.position_start,
                    assign_node.position_end,
                    "Expected variable declaration inside class",
                )
            )
            return False

        assign_node.is_static = is_static
        assign_node.target_visibility = visibility
        static_fields.append(assign_node)
        return True
