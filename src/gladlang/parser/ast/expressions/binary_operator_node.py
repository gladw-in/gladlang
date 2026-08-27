"""BinaryOperatorNode – represents binary operations (e.g., a + b, a AND b)."""


class BinaryOperatorNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.position_start = self.left_node.position_start
        self.position_end = self.right_node.position_end

    def __repr__(self):
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"
