"""ClassNode – represents class definitions with methods and static fields."""


class ClassNode:
    def __init__(
        self, class_name_token, superclass_nodes, method_nodes, static_field_nodes
    ):
        self.class_name_token = class_name_token
        self.superclass_nodes = superclass_nodes
        self.method_nodes = method_nodes
        self.static_field_nodes = static_field_nodes
        self.position_start = self.class_name_token.position_start

        if len(method_nodes) > 0:
            self.position_end = method_nodes[-1].position_end
        else:
            self.position_end = self.class_name_token.position_end
