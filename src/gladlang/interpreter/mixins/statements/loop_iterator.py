"""Helper that turns a List, String, or Dict value into an iterator of elements."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.dict import Dict
from gladlang.values.primitives.list import List
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String


class InterpreterLoopIterator:
    def get_iterator(self, iterable, start_position, end_position, context):
        if isinstance(iterable, List):
            return iterable.elements[:], None
        elif isinstance(iterable, String):

            def string_iterator(characters, context, start, end):
                for character in characters:
                    yield String(character).set_context(context).set_position(
                        start, end
                    )

            return (
                string_iterator(iterable.value, context, start_position, end_position),
                None,
            )
        elif isinstance(iterable, Dict):
            key_list = []
            for key in iterable.elements.keys():
                if (
                    isinstance(key, tuple)
                    and len(key) == 2
                    and key[0] in ("__null__", "__false__")
                ):
                    if key[0] == "__null__":
                        key_value = Number.null.copy()
                    else:
                        key_value = (Number.true if key[1] else Number.false).copy()
                elif isinstance(key, (int, float)):
                    key_value = Number(key)
                else:
                    key_value = String(key)

                key_list.append(
                    key_value.set_context(context).set_position(
                        start_position, end_position
                    )
                )
            return key_list, None

        return None, RuntimeError(
            start_position,
            end_position,
            f"Type '{type(iterable).__name__}' is not iterable (Expected List, String, or Dict)",
            context,
        )
