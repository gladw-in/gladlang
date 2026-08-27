"""ContinueNode – represents CONTINUE statement inside loops."""


class ContinueNode:
    def __init__(self, position_start, position_end):
        self.position_start = position_start
        self.position_end = position_end
