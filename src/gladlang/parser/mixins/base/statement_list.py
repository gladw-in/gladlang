"""Parses statements until a block-ending keyword."""

from gladlang.core.constants import GL_EOF, GL_KEYWORD
from gladlang.parser.ast import StatementListNode
from gladlang.parser.parse_result import ParseResult


class ParserStatementList:
    def statement_list(self, end_keywords):
        result = ParseResult()
        statements = []
        start_position = self.current_token.position_start.copy()

        while self.current_token.type != GL_EOF and not (
            self.current_token.type == GL_KEYWORD
            and self.current_token.value in end_keywords
        ):
            statements.append(result.register(self.statement()))
            if result.error:
                return result

        return result.success(
            StatementListNode(
                statements, start_position, self.current_token.position_start.copy()
            )
        )
