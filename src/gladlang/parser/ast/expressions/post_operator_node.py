"""PostOperatorNode – represents post-increment/decrement (i++, i--)."""


class PostOperatorNode:
    def __init__(self, node, operator_token):
        self.node = node
        self.operator_token = operator_token
        self.position_start = node.position_start
        self.position_end = operator_token.position_end

    def __repr__(self):
        return f"({self.node}, {self.operator_token})"
