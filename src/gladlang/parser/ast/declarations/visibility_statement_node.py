"""VisibilityStatementNode – wraps assignments with PUBLIC/PRIVATE/PROTECTED/FINAL modifiers."""


class VisibilityStatementNode:
    def __init__(self, visibility, assign_node, is_final=False):
        self.visibility = visibility
        self.assign_node = assign_node
        self.is_final = is_final
        self.position_start = assign_node.position_start
        self.position_end = assign_node.position_end
