"""Dict subscript access: d[key] get/set, with key-type and size-limit checks."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class DictElementAccess:
    __slots__ = ()

    def get_element_at(self, key):
        if not isinstance(key, (Number, String)):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "Key must be a Number or String",
                self.context,
            )

        normalized_key = self._make_key(key)
        value = self.elements.get(normalized_key)
        if value is None:
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Key '{key.value}' not found",
                self.context,
            )

        return value, None

    def set_element_at(self, key, value):
        if not isinstance(key, (Number, String)):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                "Key must be a Number or String",
                self.context,
            )

        normalized_key = self._make_key(key)
        if (
            normalized_key not in self.elements
            and len(self.elements) >= Settings.MAX_DICT_SIZE
        ):
            return None, RuntimeError(
                self.position_start,
                self.position_end,
                f"Dict size limit ({Settings.MAX_DICT_SIZE:,} entries) reached. Cannot insert more keys.",
                self.context,
            )

        self.elements[normalized_key] = value
        return value, None
