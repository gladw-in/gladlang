"""Recursive string representation for List with cycle detection."""

from gladlang.values.primitives.string import String


class ListToString:
    __slots__ = ()

    def to_string(self, visited):
        from gladlang.values.primitives.dict import Dict
        from gladlang.values.primitives.list import List

        if self in visited:
            return "[...]"

        visited.append(self)

        def format_value(item):
            if isinstance(item, (List, Dict)):
                return item.to_string(visited)

            if isinstance(item, String):
                escaped = item.value.replace("\\", "\\\\").replace('"', '\\"')
                return f'"{escaped}"'

            return repr(item)

        result_string = (
            f'[{", ".join([format_value(element) for element in self.elements])}]'
        )

        visited.pop()
        return result_string
