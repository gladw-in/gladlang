"""Function call argument list parsing: atom(arg1, arg2, ...)."""

from gladlang.core.constants import GL_COMMA, GL_RPAREN
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import CallNode
from gladlang.parser.parse_result import ParseResult


class ExpressionsCallArguments:
    def _parse_call_arguments(self, callee_node):
        result = ParseResult()
        result.register_advancement()
        self.advance()
        arguments = []
        if self.current_token.type != GL_RPAREN:
            arguments.append(result.register(self.expression()))
            if result.error:
                return result

            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()
                arguments.append(result.register(self.expression()))
                if result.error:
                    return result

        if self.current_token.type != GL_RPAREN:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ',' or ')'",
                )
            )

        result.register_advancement()
        self.advance()
        return result.success(CallNode(callee_node, arguments))
