"""Statement dispatcher – routes to the appropriate statement parser based on the current token."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.parser.parse_result import ParseResult


class StatementsDispatch:
    def statement(self):
        result = ParseResult()

        if self.current_token.type == GL_KEYWORD and self.current_token.value in (
            "PUBLIC",
            "PRIVATE",
            "PROTECTED",
            "FINAL",
        ):
            return self._parse_visibility_statement()

        if self.current_token.type == GL_KEYWORD and self.current_token.value in (
            "PRINT",
            "PRINTLN",
        ):
            return self._parse_print_statement()

        if self.current_token.matches(GL_KEYWORD, "IF"):
            return self._parse_if_statement()

        if self.current_token.matches(GL_KEYWORD, "WHILE"):
            return self.while_expression()

        if self.current_token.matches(GL_KEYWORD, "FOR"):
            return self.for_expression()

        if self.current_token.matches(GL_KEYWORD, "BREAK"):
            return self._parse_break_statement()

        if self.current_token.matches(GL_KEYWORD, "CONTINUE"):
            return self._parse_continue_statement()

        if self.current_token.matches(GL_KEYWORD, "LET"):
            return self._parse_let_statement()

        if self.current_token.matches(GL_KEYWORD, "RETURN"):
            return self._parse_return_statement()

        if self.current_token.matches(GL_KEYWORD, "DEF"):
            return self.function_definition()

        if self.current_token.matches(GL_KEYWORD, "CLASS"):
            return self.class_definition()

        if self.current_token.matches(GL_KEYWORD, "ENUM"):
            return self.enum_definition()

        if self.current_token.matches(GL_KEYWORD, "TRY"):
            return self.try_expression()

        if self.current_token.matches(GL_KEYWORD, "THROW"):
            return self._parse_throw_statement()

        if self.current_token.matches(GL_KEYWORD, "SWITCH"):
            result.register_advancement()
            self.advance()

            return self.switch_expression()

        expression = result.register(self.expression())
        if result.error:
            return result

        return result.success(expression)
