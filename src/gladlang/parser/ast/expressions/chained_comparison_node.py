"""ChainedComparisonNode – represents chained comparisons (e.g., 1 < x < 10)."""


class ChainedComparisonNode:
    def __init__(self, left_node, operators_and_expressions):
        self.left_node = left_node
        self.operators_and_expressions = operators_and_expressions
        self.position_start = left_node.position_start
        self.position_end = operators_and_expressions[-1][1].position_end

    def __repr__(self):
        return f"({self.left_node}, {self.operators_and_expressions})"
