"""Fresh global scope factory – initialises a new symbol table with built-in values."""

from gladlang.runtime.symbol_table import SymbolTable
from gladlang.values.classes.type_ import Type
from gladlang.values.functions.built_in_function import BuiltInFunction
from gladlang.values.primitives.number import Number


def get_fresh_global_scope():
    scope = SymbolTable()

    scope.set("NULL", Number.null.copy(), as_final=True)
    scope.set("FALSE", Number.false.copy(), as_final=True)
    scope.set("TRUE", Number.true.copy(), as_final=True)

    scope.set("Number", Type("Number"), as_final=True)
    scope.set("String", Type("String"), as_final=True)
    scope.set("List", Type("List"), as_final=True)
    scope.set("Dict", Type("Dict"), as_final=True)
    scope.set("Enum", Type("Enum"), as_final=True)
    scope.set("Function", Type("Function"), as_final=True)
    scope.set("Object", Type("Object"), as_final=True)

    scope.set("INPUT", BuiltInFunction("INPUT"), as_final=True)
    scope.set("STR", BuiltInFunction("STR"), as_final=True)
    scope.set("INT", BuiltInFunction("INT"), as_final=True)
    scope.set("FLOAT", BuiltInFunction("FLOAT"), as_final=True)
    scope.set("BOOL", BuiltInFunction("BOOL"), as_final=True)

    scope.set("LEN", BuiltInFunction("LEN"), as_final=True)
    scope.set("LENGTH", BuiltInFunction("LEN"), as_final=True)

    scope.set("PRINTF", BuiltInFunction("PRINTF"), as_final=True)

    scope.set("TIME", BuiltInFunction("TIME"), as_final=True)
    scope.set("TIME_SECONDS", BuiltInFunction("TIME_SECONDS"), as_final=True)
    scope.set("TIME_MILLIS", BuiltInFunction("TIME_MILLIS"), as_final=True)
    scope.set("TIME_NANOS", BuiltInFunction("TIME_NANOS"), as_final=True)

    scope.set("RANDOM", BuiltInFunction("RANDOM"), as_final=True)
    scope.set("RANDOM_FLOAT", BuiltInFunction("RANDOM_FLOAT"), as_final=True)
    scope.set("RANDOM_RANGE", BuiltInFunction("RANDOM_RANGE"), as_final=True)

    scope.set("DELAY", BuiltInFunction("DELAY"), as_final=True)

    return scope
