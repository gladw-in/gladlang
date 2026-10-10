"""Attribute access for enum members."""


class EnumMemberGetAttribute:
    __slots__ = ()

    def get_attribute(self, name_token, context=None):
        if name_token.value == "value":
            return self.value, None

        return None, self.illegal_operation()
