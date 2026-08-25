"""List subscript access: l[index] get/set."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number


class ListElementAccess:
    __slots__ = ()

    def get_element_at(self, index):
        if not isinstance(index, Number):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "List index must be a Number",
                self.context,
            )

        try:
            return self.elements[int(index.value)], None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"List index {index.value} out of bounds",
                self.context,
            )

    def set_element_at(self, index, value):
        if not isinstance(index, Number):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "List index must be a Number",
                self.context,
            )

        try:
            self.elements[int(index.value)] = value
            return value, None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"List index {index.value} out of bounds",
                self.context,
            )
