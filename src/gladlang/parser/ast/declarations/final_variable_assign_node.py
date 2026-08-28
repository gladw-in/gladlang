"""FinalVariableAssignNode – represents FINAL constant declarations."""


class FinalVariableAssignNode:
    def __init__(self, variable_name_token, value_node):
        self.variable_name_token = variable_name_token
        self.value_node = value_node
        self.position_start = self.variable_name_token.position_start
        self.position_end = self.value_node.position_end
