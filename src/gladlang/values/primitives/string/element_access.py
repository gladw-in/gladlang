"""Read a character from a string by index."""

from gladlang.core.errors import RuntimeError
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

        try:
            character = self.value[int(index.value)]
            return String(character).set_context(self.context), None
        except IndexError:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"String index {index.value} out of bounds",
                self.context,
            )
