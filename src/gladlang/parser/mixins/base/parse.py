"""Top-level entry point: parses the whole token stream into a program."""

from gladlang.core.constants import GL_EOF, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import StatementListNode
from gladlang.parser.parse_result import ParseResult


class ParserParse:
    def parse(self):
        nesting_error = self.check_nesting_depth()
        if nesting_error:
            return nesting_error

        result = ParseResult()
        statements = []
        start_position = self.current_token.position_start.copy()

        while self.current_token.type != GL_EOF:
            if self.current_token.type == GL_KEYWORD and self.current_token.value in (
                "ENDDEF",
                "ENDIF",
                "ENDCLASS",
                "ENDWHILE",
                "ENDFOR",
                "ENDENUM",
            ):
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        f"Unexpected '{self.current_token.value}'",
                    )
                )

            statement = result.register(self.statement())
            if result.error:
                return result
            statements.append(statement)

        return result.success(
            StatementListNode(
                statements, start_position, self.current_token.position_start.copy()
            )
        )
