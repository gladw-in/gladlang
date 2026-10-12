"""Context – stores execution scope, parent chain, and traceback information."""


class Context:
    __slots__ = (
        "display_name",
        "parent",
        "parent_entry_position",
        "symbol_table",
        "depth",
        "active_class",
        "is_static",
        "_tail_call_function",
        "is_repl",
        "is_function_call_context",
        "logical_parent",
        "logical_parent_entry_position",
    )

    def __init__(
        self, display_name, parent=None, parent_entry_position=None, is_repl=False
    ):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position
        self.symbol_table = None
        self.depth = (parent.depth + 1) if parent else 0
        self.active_class = parent.active_class if parent else None
        self.is_static = parent.is_static if parent else False
        self.is_repl = is_repl
        self.is_function_call_context = False
        self.logical_parent = None
        self.logical_parent_entry_position = None
