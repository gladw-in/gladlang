"""Read a character from a string by index."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.int_text import int_to_str
from gladlang.core.util.numbers import require_integer_number
from gladlang.values.primitives.number import Number


class StringElementAccess:
    __slots__ = ()

    def get_element_at(self, index):
        from gladlang.values.primitives.string import String

        if not isinstance(index, Number) or (
            hasattr(index, "_is_null") and index._is_null
        ):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "String index must be a Number",
                self.context,
            )

        index_value, error = require_integer_number(
            index.value,
            index.position_start,
            index.position_end,
            self.context,
            "String index",
        )

        if error:
            return None, error

        try:
            character = self.value[index_value]
            return String(character).set_context(self.context), None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"String index {int_to_str(index.value)} out of bounds",
                self.context,
            )
