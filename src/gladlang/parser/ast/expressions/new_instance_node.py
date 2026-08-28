"""NewInstanceNode – represents class instantiation (NEW ClassName(...))."""


class NewInstanceNode:
    def __init__(self, class_name_token, argument_nodes):
        self.class_name_token = class_name_token
        self.argument_nodes = argument_nodes
        self.position_start = self.class_name_token.position_start

        if len(argument_nodes) > 0:
            self.position_end = argument_nodes[-1].position_end
        else:
            self.position_end = self.class_name_token.position_end
