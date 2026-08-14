"""Deep-copy a List with cycle detection."""


class ListCopy:
    __slots__ = ()

    def copy(self, visited=None):
        from gladlang.values.primitives.dict import Dict
        from gladlang.values.primitives.list import List

        if visited is None:
            visited = {}

        self_identifier = id(self)
        if self_identifier in visited:
            return visited[self_identifier]

        new_list = List([])
        visited[self_identifier] = new_list

        new_list.elements = [
            (
                element.copy(visited)
                if isinstance(element, (List, Dict))
                else element.copy()
            )
            for element in self.elements
        ]

        new_list.set_position(self.position_start, self.position_end)
        new_list.set_context(self.context)
        return new_list
