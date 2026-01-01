from .errors import RTError
from .runtime import SymbolTable, Context, RTResult
from .constants import TT_IDENTIFIER
from .lexer import Token
from .nodes import *


class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def modded_by(self, other):
        return None, self.illegal_operation(other)

    def floordived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if not isinstance(other, List):
            return None, Value.illegal_operation(self, other)

        if len(self.elements) != len(other.elements):
            return Number(0).set_context(self.context), None

        for i in range(len(self.elements)):
            result, error = self.elements[i].get_comparison_eq(other.elements[i])
            if error:
                return None, error
            if not result.is_true():
                return Number(0).set_context(self.context), None

        return Number(1).set_context(self.context), None

    def get_comparison_ne(self, other):
        if not isinstance(other, List):
            return None, Value.illegal_operation(self, other)

        result, error = self.get_comparison_eq(other)
        if error:
            return None, error

        if result.is_true():
            return Number(0).set_context(self.context), None
        else:
            return Number(1).set_context(self.context), None

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def anded_by(self, other):
        is_true = self.is_true() and other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None

    def ored_by(self, other):
        is_true = self.is_true() or other.is_true()
        return Number(1 if is_true else 0).set_context(self.context), None

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def get_attr(self, name_tok):
        return None, self.illegal_operation()

    def set_attr(self, name_tok, value):
        return None, self.illegal_operation()

    def get_element_at(self, index):
        return None, self.illegal_operation()

    def set_element_at(self, index, value):
        return None, self.illegal_operation()

    def is_true(self):
        return False

    def copy(self):
        raise Exception("No copy method defined")

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RTError(self.pos_start, other.pos_end, "Illegal operation", self.context)


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        elif isinstance(other, String):
            return String(str(self.value) + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modded_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def floordived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value // other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_is(self, other):
        return Number(1 if self is other else 0).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value and other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value or other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


Number.false = Number(0)
Number.true = Number(1)
Number.null = Number(0)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        elif isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, String):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, String):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, String):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, String):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self, other)

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return String(self.value + str(other)).set_context(self.context), None

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return self.value


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        if isinstance(other, List):
            new_list = List(self.elements + other.elements)
            new_list.set_context(self.context)
            return new_list, None
        else:
            return None, self.illegal_operation(other)

    def get_element_at(self, index):
        if not isinstance(index, Number):
            return None, RTError(
                self.pos_start,
                self.pos_end,
                "List index must be a Number",
                self.context,
            )

        try:
            element = self.elements[int(index.value)]
            return element, None
        except IndexError:
            return None, RTError(
                self.pos_start,
                self.pos_end,
                f"List index {index.value} out of bounds",
                self.context,
            )

    def set_element_at(self, index, value):
        if not isinstance(index, Number):
            return None, RTError(
                self.pos_start,
                self.pos_end,
                "List index must be a Number",
                self.context,
            )

        try:
            self.elements[int(index.value)] = value
            return value, None
        except IndexError:
            return None, RTError(
                self.pos_start,
                self.pos_end,
                f"List index {index.value} out of bounds",
                self.context,
            )

    def is_true(self):
        return len(self.elements) > 0

    def copy(self):
        copy = List(self.elements[:])
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'


class Dict(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def copy(self):
        copy = Dict(self.elements.copy())
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def get_element_at(self, key):
        if not isinstance(key, (Number, String)):
            return None, RTError(
                self.pos_start,
                self.pos_end,
                "Key must be a Number or String",
                self.context,
            )

        val = self.elements.get(key.value)
        if val is None:
            return None, RTError(
                self.pos_start,
                self.pos_end,
                f"Key '{key.value}' not found",
                self.context,
            )
        return val, None

    def set_element_at(self, key, value):
        if not isinstance(key, (Number, String)):
            return None, RTError(
                self.pos_start,
                self.pos_end,
                "Key must be a Number or String",
                self.context,
            )

        self.elements[key.value] = value
        return value, None

    def __repr__(self):
        kv_strings = []
        for key, value in self.elements.items():
            kv_strings.append(f"{repr(key)}: {repr(value)}")
        return f"{{{', '.join(kv_strings)}}}"


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(self.context.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()
        if len(args) != len(arg_names):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Incorrect argument count for '{self.name}'. Expected {len(arg_names)}, got {len(args)}",
                    self.context,
                )
            )
        return res.success(None)

    def populate_args(self, arg_names, args, new_context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]

            if isinstance(arg_value, BaseFunction):
                pass
            else:
                arg_value.set_context(new_context)

            new_context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, new_context):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error:
            return res
        self.populate_args(arg_names, args, new_context)
        return res.success(None)

    def execute(self, args):
        return RTResult().failure(
            RTError(
                self.pos_start,
                self.pos_end,
                "BaseFunction cannot be executed",
                self.context,
            )
        )

    def copy(self):
        raise Exception("Cannot copy a BaseFunction")

    def __repr__(self):
        return f"<function {self.name}>"


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_name_toks, parent_context):
        super().__init__(name)
        self.body_node = body_node
        self.arg_name_toks = arg_name_toks
        self.arg_names = [tok.value for tok in arg_name_toks]
        self.context = parent_context

    def execute(self, args):
        from .interpreter import Interpreter

        res = RTResult()
        interpreter = Interpreter()

        new_context = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, new_context))
        if res.error:
            return res

        value_result = interpreter.visit(self.body_node, new_context)

        if value_result.error:
            return value_result

        if value_result.should_return:
            return res.success(value_result.return_value)

        return res.success(value_result.value or Number.null)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_name_toks, self.context)

        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy


class Class(BaseFunction):
    def __init__(self, name, superclass, methods):
        super().__init__(name)
        self.superclass = superclass
        self.methods = methods

    def execute(self, args):
        res = RTResult()
        instance = Instance(self)

        fake_init_tok = Token(TT_IDENTIFIER, "init", self.pos_start, self.pos_end)

        init_method, error = self.get_attr(fake_init_tok)

        if error:
            if len(args) > 0:
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"'{self.name}' does not have an 'init' constructor that accepts {len(args)} arguments",
                        self.context,
                    )
                )
            else:
                return res.success(instance)

        bound_init = init_method.copy().bind_to_instance(instance)
        res.register(bound_init.execute(args))
        if res.error:
            return res

        return res.success(instance)

    def get_attr(self, name_tok):
        method_name = name_tok.value
        method = self.methods.get(method_name)

        if method:
            return (
                method.copy()
                .set_context(self.context)
                .set_pos(name_tok.pos_start, name_tok.pos_end),
                None,
            )

        if self.superclass:
            return self.superclass.get_attr(name_tok)

        return None, RTError(
            name_tok.pos_start,
            name_tok.pos_end,
            f"Class '{self.name}' has no method '{method_name}'",
            self.context,
        )

    def copy(self):
        copy = Class(self.name, self.superclass, self.methods)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<class {self.name}>"


class Instance(Value):
    def __init__(self, class_ref):
        super().__init__()
        self.class_ref = class_ref
        self.symbol_table = SymbolTable()

    def get_attr(self, name_tok):
        name = name_tok.value

        value = self.symbol_table.get(name)
        if value:
            return value, None

        method, error = self.class_ref.get_attr(name_tok)
        if error:
            return None, error

        bound_method = method.copy().bind_to_instance(self)
        return bound_method, None

    def set_attr(self, name_tok, value):
        name = name_tok.value
        self.symbol_table.set(name, value)
        return value, None

    def copy(self):
        copy = Instance(self.class_ref)
        copy.symbol_table = self.symbol_table
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<{self.class_ref.name} instance>"


class BoundMethod(BaseFunction):
    def __init__(self, name, function_to_bind, instance):
        super().__init__(name)
        self.function_to_bind = function_to_bind
        self.instance = instance
        self.context = function_to_bind.context
        self.set_pos(function_to_bind.pos_start, function_to_bind.pos_end)

    def execute(self, args):
        from .interpreter import Interpreter

        res = RTResult()
        interpreter = Interpreter()

        new_context = self.function_to_bind.generate_new_context()
        new_context.symbol_table.set("SELF", self.instance)

        original_arg_names = self.function_to_bind.arg_names

        if len(original_arg_names) == 0 or original_arg_names[0] != "self":
            return res.failure(
                RTError(
                    self.function_to_bind.pos_start,
                    self.function_to_bind.pos_end,
                    f"Method '{self.name}' must have 'self' as its first argument",
                    self.context,
                )
            )

        expected_arg_names = original_arg_names[1:]

        res.register(
            self.function_to_bind.check_and_populate_args(
                expected_arg_names, args, new_context
            )
        )

        if res.error:
            return res

        value_result = interpreter.visit(self.function_to_bind.body_node, new_context)

        if value_result.error:
            return value_result

        if value_result.should_return:
            return res.success(value_result.return_value)

        return res.success(value_result.value or Number.null)

    def copy(self):
        return (
            BoundMethod(self.name, self.function_to_bind.copy(), self.instance)
            .set_context(self.context)
            .set_pos(self.pos_start, self.pos_end)
        )


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()

        if self.name == "INPUT":
            res.register(self.check_args([], args))
            if res.error:
                return res

            try:
                text = input()
            except EOFError:
                text = ""
            return res.success(String(text))

        elif self.name == "STR":
            res.register(self.check_args(["value"], args))
            if res.error:
                return res

            val = args[0]
            if isinstance(val, String):
                return res.success(String(val.value))
            else:
                return res.success(String(str(val)))

        elif self.name == "INT":
            res.register(self.check_args(["value"], args))
            if res.error:
                return res
            arg = args[0]

            if not isinstance(arg, (Number, String)):
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Argument for INT must be a Number or String, got {type(arg).__name__}",
                        self.context,
                    )
                )

            try:
                val = int(float(arg.value))
                return res.success(Number(val))
            except ValueError:
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Cannot convert '{arg.value}' to INT",
                        self.context,
                    )
                )

        elif self.name == "FLOAT":
            res.register(self.check_args(["value"], args))
            if res.error:
                return res
            arg = args[0]

            if not isinstance(arg, (Number, String)):
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Argument for FLOAT must be a Number or String, got {type(arg).__name__}",
                        self.context,
                    )
                )

            try:
                val = float(arg.value)
                return res.success(Number(val))
            except ValueError:
                return res.failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Cannot convert '{arg.value}' to FLOAT",
                        self.context,
                    )
                )

        elif self.name == "BOOL":
            res.register(self.check_args(["value"], args))
            if res.error:
                return res

            is_true = args[0].is_true()
            return res.success(Number.true if is_true else Number.false)

        return res.failure(
            RTError(
                self.pos_start,
                self.pos_end,
                f"Built-in function '{self.name}' is not defined.",
                self.context,
            )
        )

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"


def bind_to_instance(self, instance):
    return BoundMethod(self.name, self, instance)


Function.bind_to_instance = bind_to_instance
