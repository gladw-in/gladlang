"""VariableAccessNode – represents variable access (reading a variable by name)."""


class VariableAccessNode:
    def __init__(self, variable_name_token):
        self.variable_name_token = variable_name_token
        self.position_start = self.variable_name_token.position_start
        self.position_end = self.variable_name_token.position_end
