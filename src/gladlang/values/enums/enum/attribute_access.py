"""Attribute access on Enum: get case as EnumMember, cannot reassign."""

from gladlang.core.errors import RuntimeError
from gladlang.values.enums.enum_member import EnumMember


class EnumAttributeAccess:
    __slots__ = ()

    def get_attribute(self, name_token, context=None):
        name = name_token.value
        if name in self.elements_dictionary:
            value = self.elements_dictionary[name]
            member = EnumMember(self.name, name, value)

            return (
                member.set_position(
                    name_token.position_start, name_token.position_end
                ).set_context(context),
                None,
            )

        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Enum '{self.name}' has no case '{name}'",
            self.context,
        )

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Cannot reassign enum case '{name_token.value}'",
            self.context,
        )
