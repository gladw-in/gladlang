"""ForNode – represents foreach loops (FOR var IN iterable ...)."""


class ForNode:
    def __init__(self, var_name_tokens, iterable_node, body_node):
        self.var_name_tokens = var_name_tokens
        self.iterable_node = iterable_node
        self.body_node = body_node
        self.position_start = self.var_name_tokens[0].position_start
        self.position_end = self.body_node.position_end
