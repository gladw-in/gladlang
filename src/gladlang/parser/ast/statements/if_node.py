"""IfNode – represents IF / ELSE IF / ELSE conditional branches."""


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.position_start = self.cases[0][0].position_start

        if self.else_case:
            self.position_end = self.else_case.position_end
        else:
            self.position_end = self.cases[len(self.cases) - 1][1].position_end
