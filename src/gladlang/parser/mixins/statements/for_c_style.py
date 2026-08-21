"""C-style FOR loop parsing: FOR (init; condition; step) ... ENDFOR."""

from gladlang.core.constants import GL_KEYWORD, GL_RPAREN, GL_SEMI
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import CForNode


class StatementsForCStyle:
    def _parse_c_style_for(self, result, start_position):
        result.register_advancement()
        self.advance()
        init_node = None
        if self.current_token.type != GL_SEMI:
            init_node = result.register(self.statement())
            if result.error:
                return result

        if self.current_token.type != GL_SEMI:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ';'",
                )
            )

        result.register_advancement()
        self.advance()
        condition_node = None
        if self.current_token.type != GL_SEMI:
            condition_node = result.register(self.expression())
            if result.error:
                return result

        if self.current_token.type != GL_SEMI:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ';'",
                )
            )

        result.register_advancement()
        self.advance()
        step_node = None
        if self.current_token.type != GL_RPAREN:
            step_node = result.register(self.expression())
            if result.error:
                return result

        if self.current_token.type != GL_RPAREN:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ')'",
                )
            )

        result.register_advancement()
        self.advance()
        self.loop_count += 1
        body_node = result.register(self.statement_list(("ENDFOR",)))
        self.loop_count -= 1
        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "ENDFOR"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'ENDFOR'",
                )
            )

        end_position = self.current_token.position_end.copy()
        result.register_advancement()
        self.advance()

        return result.success(
            CForNode(
                init_node,
                condition_node,
                step_node,
                body_node,
                start_position,
                end_position,
            )
        )
