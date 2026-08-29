"""MutableNull – copy of FrozenNull that can be changed (used for variable assignment)."""

from gladlang.values.nulls.null_base import NullBase


class MutableNull(NullBase):
    __slots__ = ()

    def __init__(self, value, is_null=False):
        super().__init__(value, is_null)

    def copy(self):
        copy_object = MutableNull(self.value, self._is_null)
        copy_object.set_position(self.position_start, self.position_end)
        copy_object.set_context(self.context)
        return copy_object
