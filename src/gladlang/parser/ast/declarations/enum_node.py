"""EnumNode – represents enum definitions with named cases."""


class EnumNode:
    def __init__(self, enum_name_token, cases, position_start, position_end):
        self.enum_name_token = enum_name_token
        self.cases = cases
        self.position_start = position_start
        self.position_end = position_end
