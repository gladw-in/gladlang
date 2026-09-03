"""DictComprehensionNode – represents dictionary comprehensions {k: v FOR ...}."""


class DictComprehensionNode:
    def __init__(
        self,
        key_expression_node,
        value_expression_node,
        iteration_specifications,
        position_start,
        position_end,
    ):
        self.key_expression_node = key_expression_node
        self.value_expression_node = value_expression_node
        self.iteration_specifications = iteration_specifications
        self.position_start = position_start
        self.position_end = position_end
