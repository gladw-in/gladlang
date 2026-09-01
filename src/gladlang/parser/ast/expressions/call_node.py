"""CallNode – represents function or method calls with arguments."""


class CallNode:
    def __init__(self, node_to_call, argument_nodes):
        self.node_to_call = node_to_call
        self.argument_nodes = argument_nodes
        self.position_start = self.node_to_call.position_start

        if len(self.argument_nodes) > 0:
            self.position_end = self.argument_nodes[
                len(self.argument_nodes) - 1
            ].position_end
        else:
            self.position_end = self.node_to_call.position_end
