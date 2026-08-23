"""Parse class body members until ENDCLASS."""

from gladlang.core.constants import GL_EOF, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError


class ParserClassBody:
    def _parse_class_body(self, result, class_name_token):
        methods = []
        static_fields = []

        while self.current_token.type != GL_EOF and not self.current_token.matches(
            GL_KEYWORD, "ENDCLASS"
        ):
            success = self._parse_class_member(
                result, class_name_token, methods, static_fields
            )
            if not success:
                return None, None

        return methods, static_fields

    def _parse_class_member(self, result, class_name_token, methods, static_fields):
        visibility = "PUBLIC"
        is_static = False

        while self.current_token.type == GL_KEYWORD and self.current_token.value in (
            "PUBLIC",
            "PRIVATE",
            "PROTECTED",
            "STATIC",
        ):
            if self.current_token.value == "STATIC":
                is_static = True
            else:
                visibility = self.current_token.value

            result.register_advancement()
            self.advance()

        if self.current_token.matches(GL_KEYWORD, "DEF"):
            return self._parse_class_method(
                result, class_name_token, visibility, is_static, methods
            )

        elif self.current_token.matches(
            GL_KEYWORD, "LET"
        ) or self.current_token.matches(GL_KEYWORD, "FINAL"):
            return self._parse_class_field(result, visibility, is_static, static_fields)

        elif self.current_token.matches(GL_KEYWORD, "ENUM"):
            enum_node = result.register(self.enum_definition())
            if result.error:
                return False

            enum_node.visibility = visibility
            enum_node.is_static = True
            static_fields.append(enum_node)
            return True

        else:
            result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'DEF', 'LET', 'FINAL' or 'STATIC' inside class body",
                )
            )
            return False
