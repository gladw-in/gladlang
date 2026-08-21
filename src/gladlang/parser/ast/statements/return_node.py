"""ReturnNode – represents RETURN statements with optional value."""


class ReturnNode:
    def __init__(self, node_to_return, position_start, position_end):
        self.node_to_return = node_to_return
        self.position_start = position_start
        self.position_end = position_end
