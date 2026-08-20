"""Visitors for branching statements: IF/ELSE and SWITCH."""

from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterConditionals:
    def visit_IfNode(self, node, context):
        result = RuntimeResult()

        for condition, body_node in node.cases:
            condition_result = result.register(self.visit(condition, context))
            if result.error:
                return result

            if condition_result.is_true():
                expression_result = result.register(self.visit(body_node, context))
                if result.error:
                    return result

                if (
                    result.should_return
                    or result.should_break
                    or result.should_continue
                ):
                    return result

                return result.success(expression_result)

        if node.else_case:
            expression_result = result.register(self.visit(node.else_case, context))
            if result.error:
                return result

            if result.should_return or result.should_break or result.should_continue:
                return result

            return result.success(expression_result)

        return result.success(Number.null.copy())

    def visit_SwitchNode(self, node, context):
        result = RuntimeResult()

        switch_value = result.register(self.visit(node.switch_value_node, context))
        if result.error:
            return result

        for case_conditions, body_node in node.cases:
            should_execute = False

            for condition_node in case_conditions:
                case_value = result.register(self.visit(condition_node, context))
                if result.error:
                    return result

                is_equal, error = switch_value.get_comparison_eq(case_value)
                if error:
                    return result.failure(error)

                if is_equal.is_true():
                    should_execute = True
                    break

            if should_execute:
                value = result.register(self.visit(body_node, context))
                if result.error:
                    return result

                if result.should_return:
                    return result

                if result.should_break or result.should_continue:
                    return result

                return result.success(value)

        if node.default_case:
            value = result.register(self.visit(node.default_case, context))
            if (
                result.error
                or result.should_return
                or result.should_break
                or result.should_continue
            ):
                return result

            return result.success(value)

        return result.success(Number.null.copy())
