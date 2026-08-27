"""SWITCH/CASE/DEFAULT statement parsing."""

from gladlang.core.constants import GL_COLON, GL_COMMA, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import SwitchNode
from gladlang.parser.parse_result import ParseResult


class ParserSwitchExpression:
    def switch_expression(self):
        result = ParseResult()

        switch_value = result.register(self.expression())
        if result.error:
            return result

        cases = []
        default_case = None

        while self.current_token.matches(GL_KEYWORD, "CASE"):
            result.register_advancement()
            self.advance()

            case_conditions = [result.register(self.expression())]
            if result.error:
                return result

            while self.current_token.type == GL_COMMA:
                result.register_advancement()
                self.advance()
                case_conditions.append(result.register(self.expression()))
                if result.error:
                    return result

            if self.current_token.type == GL_COLON:
                result.register_advancement()
                self.advance()

            body = result.register(
                self.statement_list(("CASE", "DEFAULT", "ENDSWITCH"))
            )

            if result.error:
                return result

            cases.append((case_conditions, body))

        if self.current_token.matches(GL_KEYWORD, "DEFAULT"):
            result.register_advancement()
            self.advance()

            if self.current_token.type == GL_COLON:
                result.register_advancement()
                self.advance()

            default_case = result.register(self.statement_list(("ENDSWITCH",)))
            if result.error:
                return result

        if not self.current_token.matches(GL_KEYWORD, "ENDSWITCH"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDSWITCH'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(SwitchNode(switch_value, cases, default_case))
