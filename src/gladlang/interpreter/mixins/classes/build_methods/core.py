"""Build the methods dict for a class by running each build step in order."""


class InterpreterBuildMethodsCore:
    def _build_methods(self, result, node, context, class_value):
        methods = {}
        for method_node in node.method_nodes:
            method_name = method_node.variable_name_token.value
            method_value = self._create_method_function(
                method_node, context, class_value
            )

            add_error = self._add_method_overload(methods, method_name, method_value)
            if add_error:
                return None, add_error

            lsp_error = self._check_method_lsp(
                result, method_node, method_name, method_value, context, class_value
            )

            if lsp_error is not None:
                return None, lsp_error

        merge_error = self._merge_inherited_methods(
            result, methods, context, class_value
        )

        if merge_error is not None:
            return None, merge_error

        return methods, None
