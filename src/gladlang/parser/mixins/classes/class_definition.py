"""Parse a CLASS declaration with superclasses and body."""

from gladlang.core.constants import GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ClassNode
from gladlang.parser.parse_result import ParseResult


class ParserClassDefinition:
    def class_definition(self):
        result = ParseResult()

        if not self.current_token.matches(GL_KEYWORD, "CLASS"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'CLASS'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_IDENTIFIER:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected class name",
                )
            )

        class_name_token = self.current_token
        result.register_advancement()
        self.advance()

        superclass_nodes = self._parse_superclasses(result)
        if result.error:
            return result

        methods, static_fields = self._parse_class_body(result, class_name_token)
        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "ENDCLASS"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDCLASS'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            ClassNode(class_name_token, superclass_nodes, methods, static_fields)
        )
