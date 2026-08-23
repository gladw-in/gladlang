"""GetAttributeNode – represents attribute access (object.attr)."""


class GetAttributeNode:
    def __init__(self, object_node, attribute_name_token):
        self.object_node = object_node
        self.attribute_name_token = attribute_name_token
        self.position_start = object_node.position_start
        self.position_end = attribute_name_token.position_end
