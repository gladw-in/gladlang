"""PrintNode – represents PRINT and PRINTLN statements."""


class PrintNode:
    def __init__(
        self, print_nodes, should_newline=True, position_start=None, position_end=None
    ):
        self.print_nodes = (
            print_nodes if isinstance(print_nodes, list) else [print_nodes]
        )

        self.should_newline = should_newline
        if self.print_nodes:
            self.position_start = self.print_nodes[0].position_start
            self.position_end = self.print_nodes[-1].position_end
        else:
            self.position_start = position_start
            self.position_end = position_end
