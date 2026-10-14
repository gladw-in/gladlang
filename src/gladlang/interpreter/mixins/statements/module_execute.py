"""Interpreter module execution: lexes, parses, and interprets a module's source."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.lexer.lexer import Lexer
from gladlang.parser.parser import Parser
from gladlang.runtime.context import Context
from gladlang.runtime.modules.file_access import read_module_source
from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterModuleExecute:
    def _execute_module(self, absolute_path, cache_key, context, position_start):
        result = RuntimeResult()
        source_text = result.register(
            read_module_source(absolute_path, position_start, position_start, context)
        )

        if result.error:
            return result.error

        lexer = Lexer(absolute_path, source_text)
        tokens, error = lexer.make_tokens()
        if error:
            return RuntimeError(
                error.position_start,
                error.position_end,
                f"Error loading module '{cache_key}': {error.details}",
                context,
            )

        parser = Parser(tokens)
        try:
            ast = parser.parse()
        except RecursionError:
            return RuntimeError(
                position_start,
                position_start,
                f"Error loading module '{cache_key}': expression too complex (maximum recursion depth exceeded during parsing)",
                context,
            )

        if ast.error:
            return RuntimeError(
                ast.error.position_start,
                ast.error.position_end,
                f"Error loading module '{cache_key}': {ast.error.details}",
                context,
            )

        module_context = Context(
            f"<module {cache_key}>",
            parent=context,
            parent_entry_position=position_start,
        )

        module_context.symbol_table = get_fresh_global_scope()
        return self._run_module_ast(
            ast.node, module_context, cache_key, position_start, context
        )

    def _run_module_ast(
        self, ast_node, module_context, cache_key, position_start, context
    ):
        try:
            module_result = self.visit(ast_node, module_context)
        except RecursionError:
            return RuntimeError(
                position_start,
                position_start,
                f"Module '{cache_key}' is too deeply recursive to load",
                context,
            )
        except Exception as exception:
            return RuntimeError(
                position_start,
                position_start,
                f"Unexpected error while loading module '{cache_key}': {exception}",
                context,
            )

        if module_result.error:
            return module_result.error

        return None
