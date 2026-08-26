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
        "_tco_func",
    )

    def __init__(self, display_name, parent=None, parent_entry_position=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position
        self.symbol_table = None
        self.depth = (parent.depth + 1) if parent else 0
        self.active_class = parent.active_class if parent else None
        self.is_static = parent.is_static if parent else False
