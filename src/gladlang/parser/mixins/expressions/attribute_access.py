"""Attribute access parsing: atom.identifier."""

from gladlang.core.constants import GL_IDENTIFIER
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import GetAttributeNode
from gladlang.parser.parse_result import ParseResult


class ExpressionsAttributeAccess:
    def _parse_attribute_access(self, atom_node):
        result = ParseResult()
        result.register_advancement()
        self.advance()
        if self.current_token.type != GL_IDENTIFIER:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected identifier after '.'",
                )
            )

        attribute_name_token = self.current_token
        result.register_advancement()
        self.advance()
        return result.success(GetAttributeNode(atom_node, attribute_name_token))
