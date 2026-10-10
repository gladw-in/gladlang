"""EnumMember package – combines the enum member mixins."""

from gladlang.values.value import Value

from .core import EnumMemberCore
from .get_attribute import EnumMemberGetAttribute
from .comparison import EnumMemberComparison
from .instanceof import EnumMemberInstanceof
from .copy import EnumMemberCopy

__all__ = ["EnumMember"]


class EnumMember(
    EnumMemberCore,
    EnumMemberGetAttribute,
    EnumMemberComparison,
    EnumMemberInstanceof,
    EnumMemberCopy,
    Value,
):
    __slots__ = (
        "enum_name",
        "member_name",
        "value",
        "position_start",
        "position_end",
        "context",
    )
