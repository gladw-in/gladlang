"""Interpreter runner – orchestrates lexing, parsing, and execution in one call."""

from gladlang.core.errors import InvalidSyntaxError
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.core.util.source_detach import detach_source_from_node
from gladlang.interpreter.interpreter import Interpreter
from gladlang.lexer.lexer import Lexer
from gladlang.parser.parser import Parser
from gladlang.runtime.context import Context


def run(filename, text, context=None, instruction_limit=None):
    lexer = Lexer(filename, text)

    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)

    try:
        ast = parser.parse()
    except RecursionError:
        first = tokens[0] if tokens else None
        last = tokens[-1] if tokens else first

        return None, InvalidSyntaxError(
            first.position_start if first else None,
            last.position_end if last else None,
            "Expression too complex (maximum recursion depth exceeded during parsing)",
        )

    if ast.error:
        return None, ast.error

    if ast.node:
        detach_source_from_node(ast.node)

    interpreter = Interpreter(instruction_limit=instruction_limit)

    if context is None:
        context = Context("<program>")
        context.symbol_table = get_fresh_global_scope()

    result = interpreter.visit(ast.node, context)

    if result.should_return:
        return result.return_value, result.error

    return result.value, result.error
