"""Builds the REPL context with a fresh global scope."""

from gladlang.core.util.global_scope import get_fresh_global_scope
from gladlang.runtime.context import Context


def make_repl_context():
    repl_context = Context("<repl>", is_repl=True)
    repl_context.symbol_table = get_fresh_global_scope()

    return repl_context
