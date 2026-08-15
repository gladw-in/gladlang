"""ListNode – represents list literals [elem1, elem2, ...]."""


class ListNode:
    def __init__(self, element_nodes, position_start, position_end):
        self.element_nodes = element_nodes
        self.position_start = position_start
        self.position_end = position_end
