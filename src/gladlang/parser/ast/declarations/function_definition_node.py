"""FunctionDefinitionNode – represents function definitions (named or anonymous)."""


class FunctionDefinitionNode:
    def __init__(
        self,
        variable_name_token,
        argument_name_tokens,
        body_node,
        visibility="PUBLIC",
        is_static=False,
    ):
        self.variable_name_token = variable_name_token
        self.argument_name_tokens = argument_name_tokens
        self.body_node = body_node
        self.visibility = visibility
        self.is_static = is_static

        if self.variable_name_token:
            self.position_start = self.variable_name_token.position_start
        elif len(self.argument_name_tokens) > 0:
            self.position_start = self.argument_name_tokens[0].position_start
        else:
            self.position_start = self.body_node.position_start

        self.position_end = self.body_node.position_end
