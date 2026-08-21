"""Deep-copy Dict with cycle detection via shared visited map."""


class DictCopy:
    __slots__ = ()

    def copy(self, visited=None):
        if visited is None:
            visited = {}

        self_identifier = id(self)
        if self_identifier in visited:
            return visited[self_identifier]

        from gladlang.values.primitives.dict import Dict

        new_dictionary = Dict({})
        visited[self_identifier] = new_dictionary

        from gladlang.values.primitives.list import List

        new_dictionary.elements = {
            key: (
                value.copy(visited) if isinstance(value, (List, Dict)) else value.copy()
            )
            for key, value in self.elements.items()
        }

        new_dictionary.set_position(self.position_start, self.position_end)
        new_dictionary.set_context(self.context)
        return new_dictionary
