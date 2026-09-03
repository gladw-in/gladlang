"""Core interpreter dispatch: instruction budget, node routing, and caching."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterDispatch:
    def visit(self, node, context):
        if self.instruction_limit is not None:
            self.instruction_limit -= 1
            if self.instruction_limit <= 0:
                return RuntimeResult().failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        "Instruction budget exceeded",
                        context,
                    )
                )

        node_type = type(node)
        visit_method = self.dispatch_cache.get(node_type)

        if visit_method is None:
            method_name = f"visit_{node_type.__name__}"
            visit_method = getattr(self, method_name, self.no_visit_method)
            self.dispatch_cache[node_type] = visit_method

        try:
            result = visit_method(node, context)
        except RecursionError:
            return RuntimeResult().failure(
                RuntimeError(
                    node.position_start,
                    node.position_end,
                    "Expression too complex (maximum recursion depth exceeded)",
                    context,
                )
            )

        if isinstance(result, RuntimeResult) and (
            result.should_return
            or result.should_break
            or result.should_continue
            or result.error
        ):
            return result

        return result

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")
