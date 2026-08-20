"""TRY/CATCH/FINALLY statement parsing."""

from gladlang.core.constants import GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import TryCatchNode
from gladlang.parser.parse_result import ParseResult


class ParserTryExpression:
    def try_expression(self):
        result = ParseResult()

        if not self.current_token.matches(GL_KEYWORD, "TRY"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'TRY'",
                )
            )

        try_start_position = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        try_body = result.register(self.statement_list(("CATCH", "FINALLY", "ENDTRY")))
        if result.error:
            return result

        catch_variable = None
        catch_body = None
        finally_body = None

        if self.current_token.matches(GL_KEYWORD, "CATCH"):
            result.register_advancement()
            self.advance()

            if self.current_token.type == GL_IDENTIFIER:
                catch_variable = self.current_token
                result.register_advancement()
                self.advance()

            catch_body = result.register(self.statement_list(("FINALLY", "ENDTRY")))
            if result.error:
                return result

        if self.current_token.matches(GL_KEYWORD, "FINALLY"):
            result.register_advancement()
            self.advance()
            finally_body = result.register(self.statement_list(("ENDTRY",)))
            if result.error:
                return result

        if not self.current_token.matches(GL_KEYWORD, "ENDTRY"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDTRY'",
                )
            )

        result.register_advancement()
        self.advance()

        return result.success(
            TryCatchNode(
                try_body,
                catch_variable,
                catch_body,
                finally_body,
                try_start_position,
                self.current_token.position_start.copy(),
            )
        )
