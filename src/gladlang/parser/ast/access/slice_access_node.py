"""SliceAccessNode – represents slicing (list[start:end] or string[start:end])."""


class SliceAccessNode:
    def __init__(self, node_to_slice, start_node, end_node):
        self.node_to_slice = node_to_slice
        self.start_node = start_node
        self.end_node = end_node
        self.position_start = node_to_slice.position_start

        if end_node is not None:
            self.position_end = end_node.position_end
        elif start_node is not None:
            self.position_end = start_node.position_end
        else:
            self.position_end = node_to_slice.position_end
