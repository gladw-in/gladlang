from .runtime import RTResult, Context
from .values import Number, String, Function, Class, List, Dict
from .nodes import *
from .errors import RTError
from .constants import *


class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        result = method(node, context)

        if isinstance(result, RTResult) and (
            result.should_return
            or result.should_break
            or result.should_continue
            or result.error
        ):
            return result

        return result

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_StatementListNode(self, node, context):
        res = RTResult()
        last_value = Number.null

        for statement_node in node.statement_nodes:
            last_value = res.register(self.visit(statement_node, context))

            if (
                res.error
                or res.should_return
                or res.should_break
                or res.should_continue
            ):
                return res

        return res.success(last_value)

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error:
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_DictNode(self, node, context):
        res = RTResult()
        elements = {}

        for key_node, value_node in node.key_value_pairs:
            key = res.register(self.visit(key_node, context))
            if res.error:
                return res

            value = res.register(self.visit(value_node, context))
            if res.error:
                return res

            if isinstance(key, (Number, String)):
                elements[key.value] = value
            else:
                return res.failure(
                    RTError(
                        key_node.pos_start,
                        key_node.pos_end,
                        "Dictionary key must be a Number or String",
                        context,
                    )
                )

        return res.success(
            Dict(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_MultiVarAssignNode(self, node, context):
        res = RTResult()

        list_val = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        if not isinstance(list_val, List):
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"Cannot unpack type '{type(list_val).__name__}' (expected List)",
                    context,
                )
            )

        if len(node.var_name_toks) != len(list_val.elements):
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"ValueError: too many/not enough values to unpack (expected {len(node.var_name_toks)}, got {len(list_val.elements)})",
                    context,
                )
            )

        for i, var_name_tok in enumerate(node.var_name_toks):
            var_name = var_name_tok.value
            val = list_val.elements[i]
            context.symbol_table.set(var_name, val)

        return res.success(list_val)

    def visit_ListCompNode(self, node, context):
        res = RTResult()
        output_list = []

        iterable_val = res.register(self.visit(node.iterable_node, context))
        if res.error:
            return res

        if not isinstance(iterable_val, List):
            return res.failure(
                RTError(
                    node.iterable_node.pos_start,
                    node.iterable_node.pos_end,
                    "Expected a list",
                    context,
                )
            )

        for element in iterable_val.elements:
            context.symbol_table.set(node.var_name_tok.value, element)

            value = res.register(self.visit(node.output_expr_node, context))
            if res.error:
                return res

            output_list.append(value)

        return res.success(
            List(output_list).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_SliceAccessNode(self, node, context):
        res = RTResult()

        obj = res.register(self.visit(node.node_to_slice, context))
        if res.error:
            return res

        start_val = res.register(self.visit(node.start_node, context))
        if res.error:
            return res

        end_val = None
        if node.end_node:
            end_val = res.register(self.visit(node.end_node, context))
            if res.error:
                return res

        if isinstance(obj, (List, String)):
            if not isinstance(start_val, Number):
                return res.failure(
                    RTError(
                        node.start_node.pos_start,
                        node.start_node.pos_end,
                        "Start index must be a number",
                        context,
                    )
                )

            start_idx = int(start_val.value)
            end_idx = None

            if end_val:
                if not isinstance(end_val, Number):
                    return res.failure(
                        RTError(
                            node.end_node.pos_start,
                            node.end_node.pos_end,
                            "End index must be a number",
                            context,
                        )
                    )
                end_idx = int(end_val.value)

            if isinstance(obj, List):
                new_elements = obj.elements[start_idx:end_idx]
                return res.success(
                    List(new_elements)
                    .set_context(context)
                    .set_pos(node.pos_start, node.pos_end)
                )

            elif isinstance(obj, String):
                new_str = obj.value[start_idx:end_idx]
                return res.success(
                    String(new_str)
                    .set_context(context)
                    .set_pos(node.pos_start, node.pos_end)
                )

        return res.failure(
            RTError(
                node.pos_start,
                node.pos_end,
                f"Type {type(obj).__name__} is not sliceable",
                context,
            )
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{var_name}' is not defined",
                    context,
                )
            )

        value = value.set_pos(node.pos_start, node.pos_end)

        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_PrintNode(self, node, context):
        res = RTResult()
        value = res.register(self.visit(node.node_to_print, context))
        if res.error:
            return res

        print(value)
        return res.success(Number.null)

    def visit_IfNode(self, node, context):
        res = RTResult()

        condition_value = res.register(self.visit(node.condition_node, context))
        if res.error:
            return res

        if condition_value.is_true():
            body_value = res.register(self.visit(node.body_node, context))
            if res.error:
                return res

            if res.should_return or res.should_break or res.should_continue:
                return res

            return res.success(body_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        res = RTResult()

        iterable_value = res.register(self.visit(node.iterable_node, context))
        if res.error:
            return res

        if not isinstance(iterable_value, List):
            return res.failure(
                RTError(
                    node.iterable_node.pos_start,
                    node.iterable_node.pos_end,
                    "Iterable must be a List",
                    context,
                )
            )

        for element in iterable_value.elements:
            context.symbol_table.set(node.var_name_tok.value, element)

            value = res.register(self.visit(node.body_node, context))
            if res.error:
                return res

            if res.should_continue:
                res.should_continue = False
                continue

            if res.should_break:
                res.should_break = False
                break

            if res.should_return:
                return res

        return res.success(Number.null)

    def visit_WhileNode(self, node, context):
        res = RTResult()

        while True:
            condition_value = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res

            if not condition_value.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.error:
                return res

            if res.should_continue:
                res.should_continue = False
                continue

            if res.should_break:
                res.should_break = False
                break

            if res.should_return:
                return res

        return res.success(Number.null)

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_FunDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node

        func = Function(func_name, body_node, node.arg_name_toks, context)

        if func_name:
            context.symbol_table.set(func_name, func)

        return res.success(
            func.set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res

        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res

        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        value = res.register(self.visit(node.node_to_return, context))
        if res.error:
            return res

        return res.success_return(value)

    def visit_ClassNode(self, node, context):
        res = RTResult()
        class_name = node.class_name_tok.value

        superclass = None
        if node.superclass_node:
            superclass = res.register(self.visit(node.superclass_node, context))
            if res.error:
                return res
            if not isinstance(superclass, Class):
                return res.failure(
                    RTError(
                        node.superclass_node.pos_start,
                        node.superclass_node.pos_end,
                        "A class can only inherit from another class",
                        context,
                    )
                )

        methods = {}
        for method_node in node.method_nodes:
            method_name = method_node.var_name_tok.value
            method_value = Function(
                method_name, method_node.body_node, method_node.arg_name_toks, context
            ).set_pos(method_node.pos_start, method_node.pos_end)
            methods[method_name] = method_value

        class_value = Class(class_name, superclass, methods)
        class_value.set_context(context).set_pos(node.pos_start, node.pos_end)

        context.symbol_table.set(class_name, class_value)
        return res.success(class_value)

    def visit_NewInstanceNode(self, node, context):
        res = RTResult()

        class_name = node.class_name_tok.value
        class_value = context.symbol_table.get(class_name)

        if not class_value:
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"Class '{class_name}' is not defined",
                    context,
                )
            )

        if not isinstance(class_value, Class):
            return res.failure(
                RTError(
                    node.pos_start,
                    node.pos_end,
                    f"'{class_name}' is not a class",
                    context,
                )
            )

        args = []
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res

        instance = res.register(class_value.execute(args))
        if res.error:
            return res

        return res.success(instance.set_pos(node.pos_start, node.pos_end))

    def visit_GetAttrNode(self, node, context):
        res = RTResult()

        object = res.register(self.visit(node.object_node, context))
        if res.error:
            return res

        value, error = object.get_attr(node.attr_name_tok)
        if error:
            return res.failure(error)

        return res.success(value.set_pos(node.pos_start, node.pos_end))

    def visit_SetAttrNode(self, node, context):
        res = RTResult()

        object = res.register(self.visit(node.object_node, context))
        if res.error:
            return res

        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        new_value, error = object.set_attr(node.attr_name_tok, value)
        if error:
            return res.failure(error)

        return res.success(new_value)

    def visit_ListAccessNode(self, node, context):
        res = RTResult()

        list_val = res.register(self.visit(node.list_node, context))
        if res.error:
            return res

        index_val = res.register(self.visit(node.index_node, context))
        if res.error:
            return res

        element, error = list_val.get_element_at(index_val)
        if error:
            return res.failure(error)

        return res.success(element.copy().set_pos(node.pos_start, node.pos_end))

    def visit_ListSetNode(self, node, context):
        res = RTResult()

        list_val = res.register(self.visit(node.list_node, context))
        if res.error:
            return res

        index_val = res.register(self.visit(node.index_node, context))
        if res.error:
            return res

        value_to_set = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        new_value, error = list_val.set_element_at(index_val, value_to_set)
        if error:
            return res.failure(error)

        return res.success(new_value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_tok.type == TT_FLOORDIV:
            result, error = left.floordived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, "AND") or node.op_tok.matches(
            TT_KEYWORD, "and"
        ):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, "OR") or node.op_tok.matches(
            TT_KEYWORD, "or"
        ):
            result, error = left.ored_by(right)
        elif node.op_tok.matches(TT_KEYWORD, "IS") or node.op_tok.matches(
            TT_KEYWORD, "is"
        ):
            result, error = left.get_comparison_is(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()

        if node.op_tok.type in (TT_PLUSPLUS, TT_MINUSMINUS):
            target_node = node.node

            if isinstance(target_node, VarAccessNode):
                var_name = target_node.var_name_tok.value
                value = context.symbol_table.get(var_name)
                if not value:
                    return res.failure(
                        RTError(
                            target_node.pos_start,
                            target_node.pos_end,
                            f"'{var_name}' is not defined",
                            context,
                        )
                    )

            elif isinstance(target_node, GetAttrNode):
                obj = res.register(self.visit(target_node.object_node, context))
                if res.error:
                    return res
                value, error = obj.get_attr(target_node.attr_name_tok)
                if error:
                    return res.failure(error)

            elif isinstance(target_node, ListAccessNode):
                list_val = res.register(self.visit(target_node.list_node, context))
                if res.error:
                    return res
                index_val = res.register(self.visit(target_node.index_node, context))
                if res.error:
                    return res
                value, error = list_val.get_element_at(index_val)
                if error:
                    return res.failure(error)

            else:
                return res.failure(
                    RTError(
                        target_node.pos_start,
                        target_node.pos_end,
                        "Invalid target for increment/decrement",
                        context,
                    )
                )

            if not isinstance(value, Number):
                return res.failure(
                    RTError(
                        target_node.pos_start,
                        target_node.pos_end,
                        "Operand must be a number",
                        context,
                    )
                )

            if node.op_tok.type == TT_PLUSPLUS:
                new_value, error = value.added_to(Number(1))
            else:
                new_value, error = value.subbed_by(Number(1))

            if error:
                return res.failure(error)

            if isinstance(target_node, VarAccessNode):
                context.symbol_table.set(var_name, new_value)

            elif isinstance(target_node, GetAttrNode):
                _, error = obj.set_attr(target_node.attr_name_tok, new_value)
                if error:
                    return res.failure(error)

            elif isinstance(target_node, ListAccessNode):
                _, error = list_val.set_element_at(index_val, new_value)
                if error:
                    return res.failure(error)

            return res.success(new_value.copy().set_pos(node.pos_start, node.pos_end))

        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        number = number.copy()

        error = None
        if node.op_tok.type == TT_MINUS:
            if isinstance(number, Number):
                number, error = number.multed_by(Number(-1))
            else:
                error = RTError(
                    node.pos_start,
                    node.pos_end,
                    "Unary '-' can only be applied to numbers",
                    context,
                )
        elif node.op_tok.matches(TT_KEYWORD, "NOT"):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_PostOpNode(self, node, context):
        res = RTResult()
        target_node = node.node

        if isinstance(target_node, VarAccessNode):
            var_name = target_node.var_name_tok.value
            old_value = context.symbol_table.get(var_name)
            if not old_value:
                return res.failure(
                    RTError(
                        target_node.pos_start,
                        target_node.pos_end,
                        f"'{var_name}' is not defined",
                        context,
                    )
                )

        elif isinstance(target_node, GetAttrNode):
            obj = res.register(self.visit(target_node.object_node, context))
            if res.error:
                return res
            old_value, error = obj.get_attr(target_node.attr_name_tok)
            if error:
                return res.failure(error)

        elif isinstance(target_node, ListAccessNode):
            list_val = res.register(self.visit(target_node.list_node, context))
            if res.error:
                return res
            index_val = res.register(self.visit(target_node.index_node, context))
            if res.error:
                return res
            old_value, error = list_val.get_element_at(index_val)
            if error:
                return res.failure(error)

        else:
            return res.failure(
                RTError(
                    target_node.pos_start,
                    target_node.pos_end,
                    "Invalid target for increment/decrement",
                    context,
                )
            )

        if not isinstance(old_value, Number):
            return res.failure(
                RTError(
                    target_node.pos_start,
                    target_node.pos_end,
                    "Operand must be a number",
                    context,
                )
            )

        if node.op_tok.type == TT_PLUSPLUS:
            new_value, error = old_value.added_to(Number(1))
        else:
            new_value, error = old_value.subbed_by(Number(1))

        if error:
            return res.failure(error)

        if isinstance(target_node, VarAccessNode):
            context.symbol_table.set(var_name, new_value)

        elif isinstance(target_node, GetAttrNode):
            _, error = obj.set_attr(target_node.attr_name_tok, new_value)
            if error:
                return res.failure(error)

        elif isinstance(target_node, ListAccessNode):
            _, error = list_val.set_element_at(index_val, new_value)
            if error:
                return res.failure(error)

        return res.success(old_value.copy().set_pos(node.pos_start, node.pos_end))
