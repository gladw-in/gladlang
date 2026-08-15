"""Recursive string representation for Dict with cycle detection."""

from gladlang.values.primitives.string import String


class DictToString:
    __slots__ = ()

    def to_string(self, visited):
        from gladlang.values.primitives.dict import Dict
        from gladlang.values.primitives.list import List

        if self in visited:
            return "{...}"

        visited.append(self)
        key_value_pairs = []

        for key, value in self.elements.items():
            if isinstance(value, (List, Dict)):
                value_string = value.to_string(visited)
            elif isinstance(value, String):
                escaped = value.value.replace("\\", "\\\\").replace('"', '\\"')
                value_string = f'"{escaped}"'
            else:
                value_string = repr(value)

            if (
                isinstance(key, tuple)
                and len(key) == 2
                and key[0]
                in (
                    "__null__",
                    "__false__",
                )
            ):
                if key[0] == "__null__":
                    key_string = "null"
                else:
                    key_string = "true" if key[1] else "false"
            elif isinstance(key, str):
                key_string = f'"{key}"'
            else:
                key_string = repr(key)

            key_value_pairs.append(f"{key_string}: {value_string}")

        result_string = f"{{{', '.join(key_value_pairs)}}}"
        visited.pop()
        return result_string
