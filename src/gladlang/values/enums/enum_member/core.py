"""Core construction and setup for enum members."""


class EnumMemberCore:
    __slots__ = ()

    def __init__(self, enum_name, member_name, value):
        self.enum_name = enum_name
        self.member_name = member_name
        self.value = value
        self.position_start = self.position_end = self.context = None

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def __repr__(self):
        return f"{self.enum_name}.{self.member_name}"
