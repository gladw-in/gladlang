"""Parser mixin for EXPORT LET/FUNC/CLASS/ENUM [AS alias] declaration exports."""

from gladlang.core.constants import GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import (
    ExportNode,
    VariableAssignNode,
)
from gladlang.parser.parse_result import ParseResult


class StatementsModuleExport:
    def _parse_export_statement(self):
        result = ParseResult()
        position_start = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        if self.current_token.matches(GL_KEYWORD, "LET"):
            declaration_node = result.register(self._parse_let_statement())
            if result.error:
                return result

            if not isinstance(declaration_node, VariableAssignNode):
                return result.failure(
                    InvalidSyntaxError(
                        declaration_node.position_start,
                        declaration_node.position_end,
                        "EXPORT LET does not support destructuring",
                    )
                )

            declaration_kind, name_token = "LET", declaration_node.variable_name_token

        elif self.current_token.matches(GL_KEYWORD, "FUNC"):
            declaration_node = result.register(self.function_definition())
            if result.error:
                return result

            declaration_kind, name_token = (
                "FUNC",
                declaration_node.variable_name_token,
            )

        elif self.current_token.matches(GL_KEYWORD, "CLASS"):
            declaration_node = result.register(self.class_definition())
            if result.error:
                return result

            declaration_kind, name_token = "CLASS", declaration_node.class_name_token

        elif self.current_token.matches(GL_KEYWORD, "ENUM"):
            declaration_node = result.register(self.enum_definition())
            if result.error:
                return result

            declaration_kind, name_token = "ENUM", declaration_node.enum_name_token

        else:
            if self.current_token.type == GL_IDENTIFIER:
                return self._parse_reexport_statement(position_start)

            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'LET', 'FUNC', 'CLASS', 'ENUM', or an identifier after 'EXPORT'",
                )
            )

        exported_name = name_token.value
        position_end = declaration_node.position_end

        if self.current_token.matches(GL_KEYWORD, "AS"):
            result.register_advancement()
            self.advance()

            if self.current_token.type != GL_IDENTIFIER:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected an export alias identifier after 'AS'",
                    )
                )

            exported_name = self.current_token.value
            position_end = self.current_token.position_end
            result.register_advancement()
            self.advance()

        return result.success(
            ExportNode(
                declaration_kind,
                name_token,
                exported_name,
                declaration_node,
                position_start,
                position_end,
            )
        )
