"""ListComprehensionNode – represents list comprehensions [expression FOR ...]."""


class ListComprehensionNode:
    def __init__(
        self,
        output_expression_node,
        iteration_specifications,
        position_start,
        position_end,
    ):
        self.output_expression_node = output_expression_node
        self.iteration_specifications = iteration_specifications
        self.position_start = position_start
        self.position_end = position_end
