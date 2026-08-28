"""Parses a method definition inside a class body."""

from gladlang.core.constants import GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.lexer.token import Token


class ParserClassMethod:
    def _parse_class_method(
        self, result, class_name_token, visibility, is_static, methods
    ):
        method = result.register(self.function_definition())
        if result.error:
            return False

        if method.variable_name_token is None:
            result.failure(
                InvalidSyntaxError(
                    method.position_start,
                    method.position_end,
                    "Anonymous functions are not allowed inside a class body, methods must have a name",
                )
            )
            return False

        method.visibility = visibility
        method.is_static = is_static

        is_constructor = method.variable_name_token.value == class_name_token.value

        if not is_static:
            if (
                not len(method.argument_name_tokens)
                or method.argument_name_tokens[0].value != "THIS"
            ):
                method.argument_name_tokens.insert(
                    0,
                    Token(
                        GL_KEYWORD,
                        "THIS",
                        position_start=method.position_start,
                        position_end=method.position_start,
                    ),
                )

        if is_constructor and is_static:
            result.failure(
                InvalidSyntaxError(
                    method.position_start,
                    method.position_end,
                    f"Constructor '{class_name_token.value}' cannot be STATIC",
                )
            )
            return False

        methods.append(method)
        return True
