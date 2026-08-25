"""ListAccessNode – represents list indexing (list[index])."""


class ListAccessNode:
    def __init__(self, list_node, index_node):
        self.list_node = list_node
        self.index_node = index_node
        self.position_start = list_node.position_start
        self.position_end = index_node.position_end
