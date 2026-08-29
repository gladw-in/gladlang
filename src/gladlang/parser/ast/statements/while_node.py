"""WhileNode – represents WHILE loops."""


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.position_start = self.condition_node.position_start
        self.position_end = self.body_node.position_end
