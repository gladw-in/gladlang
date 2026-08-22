"""RuntimeResult – propagates return, break, continue, and error signals during interpretation."""


class RuntimeResult:
    __slots__ = (
        "value",
        "error",
        "return_value",
        "should_return",
        "should_break",
        "should_continue",
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.return_value = None
        self.should_return = False
        self.should_break = False
        self.should_continue = False

        return self

    def register(self, inner_result):
        if inner_result.error is None and not (
            inner_result.should_return
            or inner_result.should_break
            or inner_result.should_continue
        ):
            return inner_result.value

        if inner_result.error:
            self.error = inner_result.error

        if inner_result.should_return:
            self.return_value = inner_result.return_value
            self.should_return = True

        if inner_result.should_break:
            self.should_break = True

        if inner_result.should_continue:
            self.should_continue = True

        return inner_result.value

    def success(self, value):
        self.value = value
        return self

    def success_return(self, value):
        self.return_value = value
        self.should_return = True
        return self

    def success_break(self):
        self.should_break = True
        return self

    def success_continue(self):
        self.should_continue = True
        return self

    def failure(self, error):
        self.error = error
        return self
