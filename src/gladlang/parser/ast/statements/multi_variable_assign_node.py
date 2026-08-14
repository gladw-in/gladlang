"""MultiVariableAssignNode – represents destructuring assignment (LET [x, y] = list)."""


class MultiVariableAssignNode:
    def __init__(self, var_name_tokens, value_node, is_declaration=False):
        self.var_name_tokens = var_name_tokens
        self.value_node = value_node
        self.is_declaration = is_declaration
        self.position_start = var_name_tokens[0].position_start
        self.position_end = value_node.position_end
