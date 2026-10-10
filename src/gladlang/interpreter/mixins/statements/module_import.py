"""Interpreter visitor for IMPORT statements – loads the module and binds names into the current scope."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterModuleImport:
    def visit_ImportNode(self, node, context):
        result = RuntimeResult()
        module = result.register(
            self._load_module(
                node.source_token.value, node.position_start, node.position_end, context
            )
        )

        if result.error:
            return result

        for kind, name, alias in node.import_names:
            if kind == "namespace":
                bound_value = module
            else:
                if name not in module.exports:
                    return result.failure(
                        RuntimeError(
                            node.position_start,
                            node.position_end,
                            f"Module '{module.name}' has no export '{name}'",
                            context,
                        )
                    )

                bound_value = module.exports[name]

            if context.is_repl:
                if alias in context.symbol_table.finals:
                    return result.failure(
                        RuntimeError(
                            node.position_start,
                            node.position_end,
                            f"Cannot redeclare '{alias}': it is a constant (FINAL)",
                            context,
                        )
                    )

                if context.symbol_table.is_final_in_ancestors(alias):
                    return result.failure(
                        RuntimeError(
                            node.position_start,
                            node.position_end,
                            f"Cannot shadow constant '{alias}' with an import",
                            context,
                        )
                    )

                context.symbol_table.set(alias, bound_value)
            else:
                error = context.symbol_table.set_if_absent(alias, bound_value)
                if error:
                    return result.failure(
                        RuntimeError(
                            node.position_start,
                            node.position_end,
                            error,
                            context,
                        )
                    )

        return result.success(Number.null.copy())
