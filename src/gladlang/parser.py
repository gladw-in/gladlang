from .constants import *
from .errors import InvalidSyntaxError
from .nodes import *
from .lexer import Token


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type != TT_EOF:
            if self.current_tok.type == TT_KEYWORD and self.current_tok.value in (
                "ENDEF",
                "ENDIF",
                "ENDCLASS",
                "ENDWHILE",
                "ENDFOR",
            ):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        f"Unexpected '{self.current_tok.value}'",
                    )
                )

            statement = res.register(self.statement())
            if res.error:
                return res
            statements.append(statement)

        return res.success(
            StatementListNode(statements, pos_start, self.current_tok.pos_start.copy())
        )

    def statement_list(self, end_keywords):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type != TT_EOF and not (
            self.current_tok.type == TT_KEYWORD
            and self.current_tok.value in end_keywords
        ):
            statements.append(res.register(self.statement()))
            if res.error:
                return res

        return res.success(
            StatementListNode(statements, pos_start, self.current_tok.pos_start.copy())
        )

    def statement(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "PRINT"):
            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(PrintNode(expr))

        if self.current_tok.matches(TT_KEYWORD, "IF"):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "THEN"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'THEN'",
                    )
                )

            res.register_advancement()
            self.advance()

            body = res.register(self.statement_list(("ENDIF",)))

            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "ENDIF"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'ENDIF'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(IfNode(condition, body))

        if self.current_tok.matches(TT_KEYWORD, "WHILE"):
            return self.while_expr()

        if self.current_tok.matches(TT_KEYWORD, "FOR"):
            return self.for_expr()

        if self.current_tok.matches(TT_KEYWORD, "BREAK"):
            pos_start = self.current_tok.pos_start.copy()
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "CONTINUE"):
            pos_start = self.current_tok.pos_start.copy()
            res.register_advancement()
            self.advance()
            return res.success(
                ContinueNode(pos_start, self.current_tok.pos_start.copy())
            )

        if self.current_tok.matches(TT_KEYWORD, "LET"):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_LSQUARE:
                res.register_advancement()
                self.advance()

                var_names = []

                if self.current_tok.type == TT_IDENTIFIER:
                    var_names.append(self.current_tok)
                    res.register_advancement()
                    self.advance()

                    while self.current_tok.type == TT_COMMA:
                        res.register_advancement()
                        self.advance()

                        if self.current_tok.type == TT_IDENTIFIER:
                            var_names.append(self.current_tok)
                            res.register_advancement()
                            self.advance()
                        else:
                            return res.failure(
                                InvalidSyntaxError(
                                    self.current_tok.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected identifier",
                                )
                            )

                if self.current_tok.type != TT_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ']'",
                        )
                    )
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_EQ:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected '='",
                        )
                    )
                res.register_advancement()
                self.advance()

                expr = res.register(self.expr())
                if res.error:
                    return res

                return res.success(MultiVarAssignNode(var_names, expr))

            elif self.current_tok.type == TT_IDENTIFIER:
                var_name = self.current_tok
                res.register_advancement()
                self.advance()

                if self.current_tok.type == TT_LSQUARE:
                    res.register_advancement()
                    self.advance()

                    index_expr = res.register(self.expr())
                    if res.error:
                        return res

                    if self.current_tok.type != TT_RSQUARE:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ']'",
                            )
                        )
                    res.register_advancement()
                    self.advance()

                    if self.current_tok.type != TT_EQ:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected '='",
                            )
                        )
                    res.register_advancement()
                    self.advance()

                    value_expr = res.register(self.expr())
                    if res.error:
                        return res

                    return res.success(
                        ListSetNode(VarAccessNode(var_name), index_expr, value_expr)
                    )

                elif self.current_tok.type == TT_EQ:
                    res.register_advancement()
                    self.advance()

                    expr = res.register(self.expr())
                    if res.error:
                        return res
                    return res.success(VarAssignNode(var_name, expr))

                else:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected '=' or '['",
                        )
                    )

            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier or '['",
                    )
                )

        if self.current_tok.matches(TT_KEYWORD, "RETURN"):
            res.register_advancement()
            self.advance()
            pos_start = self.current_tok.pos_start.copy()

            expr = res.register(self.expr())
            if res.error:
                return res

            return res.success(ReturnNode(expr, pos_start, expr.pos_end))

        if self.current_tok.matches(TT_KEYWORD, "DEF"):
            return self.fun_def()

        if self.current_tok.matches(TT_KEYWORD, "CLASS"):
            return self.class_def()

        expr = res.register(self.expr())
        if res.error:
            return res
        return res.success(expr)

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FOR"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'FOR'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected identifier (variable name)",
                )
            )

        var_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if not self.current_tok.matches(TT_KEYWORD, "IN"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'IN'",
                )
            )

        res.register_advancement()
        self.advance()

        iterable_node = res.register(self.expr())
        if res.error:
            return res

        body_node = res.register(self.statement_list(("ENDFOR",)))
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "ENDFOR"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'ENDFOR'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(ForNode(var_name_tok, iterable_node, body_node))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "WHILE"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'WHILE'",
                )
            )

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        body = res.register(self.statement_list(("ENDWHILE",)))
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "ENDWHILE"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'ENDWHILE'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(WhileNode(condition, body))

    def expr(self):
        return self.bin_op(
            self.comp_expr,
            (
                (TT_KEYWORD, "AND"),
                (TT_KEYWORD, "OR"),
                (TT_KEYWORD, "and"),
                (TT_KEYWORD, "or"),
            ),
        )

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "NOT"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.arith_expr())
        if res.error:
            return res

        ops = []

        while self.current_tok.type in (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE) or (
            self.current_tok.type == TT_KEYWORD
            and self.current_tok.value in ("is", "IS")
        ):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right_expr = res.register(self.arith_expr())
            if res.error:
                return res

            ops.append((op_tok, right_expr))

        if not ops:
            return res.success(node)

        left_node = node
        first_op, first_right = ops[0]

        result_node = BinOpNode(left_node, first_op, first_right)

        prev_right = first_right

        for i in range(1, len(ops)):
            op_tok, right_expr = ops[i]

            next_comp = BinOpNode(prev_right, op_tok, right_expr)

            and_tok = Token(
                TT_KEYWORD, "and", pos_start=op_tok.pos_start, pos_end=op_tok.pos_end
            )

            result_node = BinOpNode(result_node, and_tok, next_comp)
            prev_right = right_expr

        return res.success(result_node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD, TT_FLOORDIV))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_PLUSPLUS, TT_MINUSMINUS):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.call())
            if res.error:
                return res

            if not isinstance(node, (VarAccessNode, GetAttrNode, ListAccessNode)):
                return res.failure(
                    InvalidSyntaxError(
                        node.pos_start,
                        op_tok.pos_end,
                        "Invalid target for pre-increment/decrement operator",
                    )
                )

            return res.success(UnaryOpNode(op_tok, node))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        while True:
            if self.current_tok.type == TT_LPAREN:
                res.register_advancement()
                self.advance()
                arg_nodes = []

                if self.current_tok.type != TT_RPAREN:
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                    while self.current_tok.type == TT_COMMA:
                        res.register_advancement()
                        self.advance()

                        arg_nodes.append(res.register(self.expr()))
                        if res.error:
                            return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ',' or ')'",
                        )
                    )

                res.register_advancement()
                self.advance()
                atom = CallNode(atom, arg_nodes)

            elif self.current_tok.type == TT_DOT:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier after '.'",
                        )
                    )

                attr_name_tok = self.current_tok
                res.register_advancement()
                self.advance()

                atom = GetAttrNode(atom, attr_name_tok)

            elif self.current_tok.type == TT_LSQUARE:
                res.register_advancement()
                self.advance()

                start_node = res.register(self.expr())
                if res.error:
                    return res

                if self.current_tok.type == TT_COLON:
                    res.register_advancement()
                    self.advance()

                    end_node = None
                    if self.current_tok.type != TT_RSQUARE:
                        end_node = res.register(self.expr())
                        if res.error:
                            return res

                    if self.current_tok.type != TT_RSQUARE:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ']'",
                            )
                        )

                    res.register_advancement()
                    self.advance()
                    atom = SliceAccessNode(atom, start_node, end_node)

                else:
                    if self.current_tok.type != TT_RSQUARE:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ']'",
                            )
                        )

                    res.register_advancement()
                    self.advance()
                    atom = ListAccessNode(atom, start_node)

            else:
                break

        if self.current_tok.type in (TT_PLUSPLUS, TT_MINUSMINUS):
            if not isinstance(atom, (VarAccessNode, GetAttrNode, ListAccessNode)):
                return res.failure(
                    InvalidSyntaxError(
                        atom.pos_start,
                        self.current_tok.pos_end,
                        "Invalid target for post-increment/decrement operator",
                    )
                )

            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            atom = PostOpNode(atom, op_tok)

        if self.current_tok.type == TT_EQ:
            if isinstance(atom, GetAttrNode):
                res.register_advancement()
                self.advance()
                value = res.register(self.expr())
                if res.error:
                    return res
                return res.success(
                    SetAttrNode(atom.object_node, atom.attr_name_tok, value)
                )

            elif isinstance(atom, ListAccessNode):
                res.register_advancement()
                self.advance()
                value = res.register(self.expr())
                if res.error:
                    return res
                return res.success(ListSetNode(atom.list_node, atom.index_node, value))

            else:
                return res.failure(
                    InvalidSyntaxError(
                        atom.pos_start, atom.pos_end, "Invalid assignment target"
                    )
                )

        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type == TT_LBRACE:
            return self.dict_expr()

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.matches(TT_KEYWORD, "SELF"):
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )

        elif tok.type == TT_LSQUARE:
            return self.list_expr()

        elif tok.matches(TT_KEYWORD, "DEF"):
            return self.fun_def()

        elif tok.matches(TT_KEYWORD, "CLASS"):
            return self.class_def()

        elif tok.matches(TT_KEYWORD, "NEW"):
            return self.new_instance()

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start,
                tok.pos_end,
                "Expected int, float, string, identifier, '+', '-', '++', '--', '(', '[', 'DEF', 'CLASS', or 'NEW'",
            )
        )

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '['"
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
            return res.success(
                ListNode([], pos_start, self.current_tok.pos_start.copy())
            )

        first_expr = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORD, "FOR"):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if not self.current_tok.matches(TT_KEYWORD, "IN"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'IN'",
                    )
                )

            res.register_advancement()
            self.advance()

            iterable = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ']'",
                    )
                )

            res.register_advancement()
            self.advance()

            return res.success(ListCompNode(first_expr, var_name, iterable))

        element_nodes.append(first_expr)

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()

            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res

        if self.current_tok.type != TT_RSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or ']'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(
            ListNode(element_nodes, pos_start, self.current_tok.pos_start.copy())
        )

    def fun_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "DEF"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'DEF'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected '(' after function name",
                    )
                )
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected '('",
                    )
                )

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type != TT_RPAREN:
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )

            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier",
                        )
                    )

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

        if self.current_tok.type != TT_RPAREN:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or ')'",
                )
            )

        res.register_advancement()
        self.advance()

        body = res.register(self.statement_list(("ENDEF",)))

        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "ENDEF"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'ENDEF'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(FunDefNode(var_name_tok, arg_name_toks, body))

    def class_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "CLASS"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'CLASS'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected class name",
                )
            )

        class_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        superclass_node = None
        if self.current_tok.matches(TT_KEYWORD, "INHERITS"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected superclass name",
                    )
                )
            superclass_node = VarAccessNode(self.current_tok)
            res.register_advancement()
            self.advance()

        method_nodes = []

        while self.current_tok.type != TT_EOF and not self.current_tok.matches(
            TT_KEYWORD, "ENDCLASS"
        ):
            if not self.current_tok.matches(TT_KEYWORD, "DEF"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'DEF' (methods) inside class body",
                    )
                )

            method_node = res.register(self.fun_def())
            if res.error:
                return res
            if not method_node.var_name_tok:
                return res.failure(
                    InvalidSyntaxError(
                        method_node.pos_start,
                        method_node.pos_end,
                        "Methods inside a class must have a name",
                    )
                )

            method_nodes.append(method_node)

        if not self.current_tok.matches(TT_KEYWORD, "ENDCLASS"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'ENDCLASS'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(ClassNode(class_name_tok, superclass_node, method_nodes))

    def new_instance(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "NEW"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'NEW'",
                )
            )

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected class name",
                )
            )

        class_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '(' after class name for 'NEW'",
                )
            )

        res.register_advancement()
        self.advance()
        arg_nodes = []

        if self.current_tok.type != TT_RPAREN:
            arg_nodes.append(res.register(self.expr()))
            if res.error:
                return res

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or ')'",
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(NewInstanceNode(class_name_tok, arg_nodes))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while (
            self.current_tok.type in ops
            or (self.current_tok.type, self.current_tok.value) in ops
        ):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def dict_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        res.register_advancement()
        self.advance()

        kv_pairs = []

        if self.current_tok.type != TT_RBRACE:
            key = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type != TT_COLON:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ':'",
                    )
                )

            res.register_advancement()
            self.advance()

            value = res.register(self.expr())
            if res.error:
                return res

            kv_pairs.append((key, value))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type == TT_RBRACE:
                    break

                key = res.register(self.expr())
                if res.error:
                    return res

                if self.current_tok.type != TT_COLON:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ':'",
                        )
                    )

                res.register_advancement()
                self.advance()

                value = res.register(self.expr())
                if res.error:
                    return res

                kv_pairs.append((key, value))

        if self.current_tok.type != TT_RBRACE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"
                )
            )

        res.register_advancement()
        self.advance()

        return res.success(
            DictNode(kv_pairs, pos_start, self.current_tok.pos_start.copy())
        )
