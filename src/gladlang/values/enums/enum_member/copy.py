"""Copying of an enum member."""


class EnumMemberCopy:
    __slots__ = ()

    def copy(self):
        from . import EnumMember

        member_copy = EnumMember(self.enum_name, self.member_name, self.value)

        return member_copy.set_position(
            self.position_start, self.position_end
        ).set_context(self.context)
