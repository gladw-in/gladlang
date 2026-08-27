"""Visibility-modifier statement parsing (PUBLIC/PRIVATE/PROTECTED/FINAL)."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    SetAttributeNode,
    VariableAssignNode,
    VisibilityStatementNode,
)
from gladlang.parser.parse_result import ParseResult


class StatementsVisibility:
    def _parse_visibility_statement(self):
        result = ParseResult()

        visibility = "PUBLIC"
        is_final = False
        while self.current_token.type == GL_KEYWORD and self.current_token.value in (
            "PUBLIC",
            "PRIVATE",
            "PROTECTED",
            "FINAL",
        ):
            if self.current_token.value == "FINAL":
                is_final = True
            else:
                visibility = self.current_token.value

            result.register_advancement()
            self.advance()

        if self.current_token.matches(GL_KEYWORD, "ENUM"):
            enum_node = result.register(self.enum_definition())
            if result.error:
                return result

            enum_node.visibility = visibility

            return result.success(enum_node)

        expression = result.register(self.expression())
        if result.error:
            return result

        if isinstance(expression, (SetAttributeNode, VariableAssignNode)):
            return result.success(
                VisibilityStatementNode(visibility, expression, is_final=is_final)
            )

        return result.failure(
            InvalidSyntaxError(
                expression.position_start,
                expression.position_end,
                "Visibility modifiers can only be used with variable or attribute assignments",
            )
        )
