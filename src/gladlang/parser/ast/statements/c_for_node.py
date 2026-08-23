"""CForNode – represents C-style FOR loops (FOR (init; cond; step) ...)."""


class CForNode:
    def __init__(
        self,
        init_node,
        condition_node,
        step_node,
        body_node,
        position_start,
        position_end,
    ):
        self.init_node = init_node
        self.condition_node = condition_node
        self.step_node = step_node
        self.body_node = body_node
        self.position_start = position_start
        self.position_end = position_end
