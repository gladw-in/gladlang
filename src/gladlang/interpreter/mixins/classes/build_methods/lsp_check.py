"""Check that a method is not more private than the same method in a parent class."""

from gladlang.core.errors import RuntimeError


class InterpreterBuildMethodsLspCheck:
    def _check_method_lsp(
        self, result, method_node, method_name, method_value, context, class_value
    ):
        parent_method = None
        for ancestor in class_value.mro:
            if ancestor == class_value:
                continue

            if method_name in ancestor.methods:
                parent_method = ancestor.methods[method_name]
                break

        if parent_method:
            visibility_levels = {"PUBLIC": 3, "PROTECTED": 2, "PRIVATE": 1}
            parent_visibility_score = visibility_levels.get(parent_method.visibility, 3)

            child_visibility_score = visibility_levels.get(method_value.visibility, 3)

            if child_visibility_score < parent_visibility_score:
                return result.failure(
                    RuntimeError(
                        method_node.position_start,
                        method_node.position_end,
                        f"Method '{method_name}' cannot be more restrictive than parent method (LSP Violation)",
                        context,
                    )
                )

        return None
