"""VariableAssignNode – represents variable assignment (LET x = expression)."""


class VariableAssignNode:
    def __init__(self, variable_name_token, value_node, is_declaration=False):
        self.variable_name_token = variable_name_token
        self.value_node = value_node
        self.is_declaration = is_declaration
        self.position_start = self.variable_name_token.position_start
        self.position_end = self.value_node.position_end
