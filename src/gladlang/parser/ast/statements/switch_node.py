"""SwitchNode – represents SWITCH / CASE / DEFAULT statements."""


class SwitchNode:
    def __init__(self, switch_value_node, cases, default_case):
        self.switch_value_node = switch_value_node
        self.cases = cases
        self.default_case = default_case
        self.position_start = switch_value_node.position_start

        if default_case:
            self.position_end = default_case.position_end
        elif cases:
            self.position_end = cases[-1][1].position_end
        else:
            self.position_end = switch_value_node.position_end
