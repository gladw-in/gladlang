"""TernaryOperatorNode – represents conditional expressions (cond ? true : false)."""


class TernaryOperatorNode:
    def __init__(self, condition_node, true_case_node, false_case_node):
        self.condition_node = condition_node
        self.true_case_node = true_case_node
        self.false_case_node = false_case_node
        self.position_start = condition_node.position_start
        self.position_end = false_case_node.position_end

    def __repr__(self):
        return (
            f"({self.condition_node} ? {self.true_case_node} : {self.false_case_node})"
        )
