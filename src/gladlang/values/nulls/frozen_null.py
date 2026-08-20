"""FrozenNull – immutable NULL, TRUE, FALSE singletons (can't be modified)."""

from gladlang.values.nulls.null_base import NullBase
from gladlang.values.nulls.mutable_null import MutableNull


class FrozenNull(NullBase):
    __slots__ = ()

    def __init__(self, value, is_null=False):
        super().__init__(value, is_null)

    def set_position(self, position_start=None, position_end=None):
        return self

    def set_context(self, context=None):
        return self

    def copy(self):
        return MutableNull(self.value, self._is_null)
