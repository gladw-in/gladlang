"""List subscript access: l[index] get/set."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.int_text import int_to_str
from gladlang.core.util.numbers import require_integer_number
from gladlang.values.primitives.number import Number


class ListElementAccess:
    __slots__ = ()

    def get_element_at(self, index):
        if not isinstance(index, Number) or (
            hasattr(index, "_is_null") and index._is_null
        ):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "List index must be a Number",
                self.context,
            )

        index_value, error = require_integer_number(
            index.value,
            index.position_start,
            index.position_end,
            self.context,
            "List index",
        )
        if error:
            return None, error

        try:
            return self.elements[index_value], None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"List index {int_to_str(index.value)} out of bounds",
                self.context,
            )

    def set_element_at(self, index, value):
        if not isinstance(index, Number) or (
            hasattr(index, "_is_null") and index._is_null
        ):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "List index must be a Number",
                self.context,
            )

        index_value, error = require_integer_number(
            index.value,
            index.position_start,
            index.position_end,
            self.context,
            "List index",
        )

        if error:
            return None, error

        try:
            self.elements[index_value] = value
            return value, None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"List index {int_to_str(index.value)} out of bounds",
                self.context,
            )
