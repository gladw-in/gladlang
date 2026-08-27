"""Parse a function definition with name, arguments, and body."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import FunctionDefinitionNode
from gladlang.parser.parse_result import ParseResult


class ParserFunctionDefinition:
    def function_definition(self):
        result = ParseResult()

        if not self.current_token.matches(GL_KEYWORD, "DEF"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'DEF'",
                )
            )

        result.register_advancement()
        self.advance()

        function_name_token = self._parse_function_name(result)
        if result.error:
            return result

        result.register_advancement()
        self.advance()

        argument_tokens = self._parse_function_arguments(result)
        if result.error:
            return result

        result.register_advancement()
        self.advance()

        saved_loop_count = self.loop_count
        self.loop_count = 0
        self.function_count += 1

        body = result.register(self.statement_list(("ENDDEF",)))

        self.function_count -= 1
        self.loop_count = saved_loop_count

        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "ENDDEF"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDDEF'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            FunctionDefinitionNode(function_name_token, argument_tokens, body)
        )
