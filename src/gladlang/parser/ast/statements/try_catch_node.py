"""TryCatchNode – represents TRY / CATCH / FINALLY exception handling blocks."""


class TryCatchNode:
    def __init__(
        self,
        try_body_node,
        catch_variable_node,
        catch_body_node,
        finally_body_node,
        position_start,
        position_end,
    ):
        self.try_body_node = try_body_node
        self.catch_variable_node = catch_variable_node
        self.catch_body_node = catch_body_node
        self.finally_body_node = finally_body_node
        self.position_start = position_start
        self.position_end = position_end
