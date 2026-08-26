"""Subscript and slice access parsing: atom[index] and atom[start:end]."""

from gladlang.core.constants import GL_COLON, GL_RSQUARE
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ListAccessNode, SliceAccessNode
from gladlang.parser.parse_result import ParseResult


class ExpressionsSubscriptAccess:
    def _parse_subscript_access(self, base_node):
        result = ParseResult()
        result.register_advancement()
        self.advance()
        start_node = None
        if self.current_token.type not in (GL_COLON, GL_RSQUARE):
            start_node = result.register(self.expression())
            if result.error:
                return result

        if self.current_token.type == GL_COLON:
            result.register_advancement()
            self.advance()
            end_node = None
            if self.current_token.type != GL_RSQUARE:
                end_node = result.register(self.expression())
                if result.error:
                    return result

            if self.current_token.type != GL_RSQUARE:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ']'",
                    )
                )

            result.register_advancement()
            self.advance()
            return result.success(SliceAccessNode(base_node, start_node, end_node))
        else:
            if start_node is None:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected expression before ']'",
                    )
                )

            if self.current_token.type != GL_RSQUARE:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ']'",
                    )
                )

            result.register_advancement()
            self.advance()
            return result.success(ListAccessNode(base_node, start_node))
