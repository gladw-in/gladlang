"""TailCall – marker for tail call optimisation (TCO) in recursive functions."""


class TailCall:
    __slots__ = ("function", "arguments")

    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments
