"""IF / ELSE IF / ELSE statement parsing."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import IfNode
from gladlang.parser.parse_result import ParseResult


class StatementsIf:
    def _parse_if_statement(self):
        result = ParseResult()

        result.register_advancement()
        self.advance()

        cases = []
        else_case = None

        condition = result.register(self.expression())
        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "THEN"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'THEN'",
                )
            )

        result.register_advancement()
        self.advance()

        body = result.register(self.statement_list(("ELSE", "ENDIF")))
        if result.error:
            return result

        cases.append((condition, body))

        while self.current_token.matches(GL_KEYWORD, "ELSE"):
            next_index = self.token_index + 1
            next_token_is_if = (
                next_index < len(self.tokens)
                and self.tokens[next_index].matches(GL_KEYWORD, "IF")
                and self.tokens[next_index].position_start.line
                == self.current_token.position_start.line
            )

            if next_token_is_if:
                result.register_advancement()
                self.advance()
                result.register_advancement()
                self.advance()
                condition = result.register(self.expression())
                if result.error:
                    return result

                if not self.current_token.matches(GL_KEYWORD, "THEN"):
                    return result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "Expected 'THEN' after ELSE IF",
                        )
                    )

                result.register_advancement()
                self.advance()
                body = result.register(self.statement_list(("ELSE", "ENDIF")))
                if result.error:
                    return result

                cases.append((condition, body))
            else:
                result.register_advancement()
                self.advance()
                else_case = result.register(self.statement_list(("ENDIF",)))
                if result.error:
                    return result

                break

        if not self.current_token.matches(GL_KEYWORD, "ENDIF"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDIF'",
                )
            )

        result.register_advancement()
        self.advance()
        return result.success(IfNode(cases, else_case))
