"""Statement-visitor mixins, composed into a single class."""

from .c_for_loop import InterpreterCForLoop
from .conditionals import InterpreterConditionals
from .for_loop import InterpreterForLoop
from .jump_statements import InterpreterJumpStatements
from .loop_iterator import InterpreterLoopIterator
from .loop_unpack import InterpreterLoopUnpack
from .module_claim import InterpreterModuleClaim
from .module_body import InterpreterModuleBody
from .module_execute import InterpreterModuleExecute
from .module_export import InterpreterModuleExport
from .module_export_guard import InterpreterModuleExportGuard
from .module_import import InterpreterModuleImport
from .module_reexport import InterpreterModuleReExport
from .print_statement import InterpreterPrintStatement
from .statement_list import InterpreterStatementList
from .try_catch import InterpreterTryCatch
from .try_catch_body import InterpreterTryCatchBody
from .while_loop import InterpreterWhileLoop


class InterpreterStatements(
    InterpreterStatementList,
    InterpreterConditionals,
    InterpreterLoopUnpack,
    InterpreterModuleClaim,
    InterpreterModuleBody,
    InterpreterModuleExecute,
    InterpreterModuleExport,
    InterpreterModuleExportGuard,
    InterpreterModuleImport,
    InterpreterModuleReExport,
    InterpreterLoopIterator,
    InterpreterForLoop,
    InterpreterWhileLoop,
    InterpreterCForLoop,
    InterpreterJumpStatements,
    InterpreterTryCatch,
    InterpreterTryCatchBody,
    InterpreterPrintStatement,
):
    pass


__all__ = ["InterpreterStatements"]
