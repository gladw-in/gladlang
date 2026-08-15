"""Dict `+` merges two dicts (right-hand entries win on key collision)."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class DictArithmetic:
    __slots__ = ()

    def added_to(self, other):
        from gladlang.values.primitives.dict import Dict

        if isinstance(other, Dict):
            new_length = len(self.elements) + len(other.elements)
            if new_length > Settings.MAX_DICT_SIZE:
                return None, RuntimeError(
                    other.position_start,
                    other.position_end,
                    f"Dict merge result ({new_length}) exceeds maximum allowed size ({Settings.MAX_DICT_SIZE})",
                    self.context,
                )

            from gladlang.values.primitives.list import List

            visited_map = {}

            def safe_copy(item):
                if isinstance(item, (List, Dict)):
                    return item.copy(visited_map)

                return item.copy()

            merged = {key: safe_copy(value) for key, value in self.elements.items()}
            merged.update(
                {key: safe_copy(value) for key, value in other.elements.items()}
            )

            new_dictionary = Dict(merged)
            new_dictionary.set_context(self.context)

            return new_dictionary, None
        return None, self._illegal(other)
