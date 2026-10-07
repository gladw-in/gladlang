"""ExportNode – represents EXPORT LET/FUNC/CLASS [AS alias] statements."""


class ExportNode:
    def __init__(
        self,
        declaration_kind,
        name_token,
        exported_name,
        declaration_node,
        position_start,
        position_end,
    ):
        self.declaration_kind = declaration_kind
        self.name_token = name_token
        self.exported_name = exported_name
        self.declaration_node = declaration_node
        self.position_start = position_start
        self.position_end = position_end
