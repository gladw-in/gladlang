"""Instance – composed from multiple mixins."""

from .core import InstanceCore
from .check_access import InstanceCheckAccess
from .get_attribute import InstanceGetAttribute
from .get_attribute_class_member import InstanceGetAttributeClassMember
from .set_attribute import InstanceSetAttribute
from .set_attribute_reassign import InstanceSetAttributeReassign
from .comparisons import InstanceComparisons


class Instance(
    InstanceCheckAccess,
    InstanceGetAttribute,
    InstanceGetAttributeClassMember,
    InstanceSetAttribute,
    InstanceSetAttributeReassign,
    InstanceComparisons,
    InstanceCore,
):
    __slots__ = ()


__all__ = ["Instance"]
