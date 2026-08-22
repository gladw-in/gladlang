"""ThrowNode – represents THROW statements for raising errors."""


class ThrowNode:
    def __init__(self, node_to_throw, position_start, position_end):
        self.node_to_throw = node_to_throw
        self.position_start = position_start
        self.position_end = position_end
