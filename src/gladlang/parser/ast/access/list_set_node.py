"""ListSetNode – represents list element assignment (list[index] = value)."""


class ListSetNode:
    def __init__(self, list_node, index_node, value_node, compound_operator=None):
        self.list_node = list_node
        self.index_node = index_node
        self.value_node = value_node
        self.compound_operator = compound_operator
        self.position_start = list_node.position_start
        self.position_end = value_node.position_end
