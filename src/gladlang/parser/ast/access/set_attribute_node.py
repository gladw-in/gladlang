"""SetAttributeNode – represents attribute assignment (object.attr = value)."""


class SetAttributeNode:
    def __init__(
        self, object_node, attribute_name_token, value_node, compound_operator=None
    ):
        self.object_node = object_node
        self.attribute_name_token = attribute_name_token
        self.value_node = value_node
        self.compound_operator = compound_operator
        self.position_start = object_node.position_start
        self.position_end = value_node.position_end
