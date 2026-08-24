"""Core Dict with key normalization and value overrides."""

from gladlang.core.errors import RuntimeError
from gladlang.values.primitives.number import Number
from gladlang.values.primitives.string import String
from gladlang.values.value import Value


class DictCore(Value):
    __slots__ = ("elements", "position_start", "position_end", "context")

    def __init__(self, elements):
        self.elements = {}

        for raw_key, value in elements.items():
            self.elements[self._make_key(raw_key)] = value

        self.position_start = None
        self.position_end = None
        self.context = None

    def _make_key(self, raw_key):
        if hasattr(raw_key, "_is_null"):
            if raw_key._is_null:
                return ("__null__", raw_key.value)
            else:
                return ("__false__", raw_key.value)

        if isinstance(raw_key, (String, Number)):
            return raw_key.value

        return raw_key

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def is_true(self):
        return len(self.elements) > 0

    def execute(self, arguments, interpreter=None, calling_context=None):
        from gladlang.runtime.runtime_result import RuntimeResult

        return RuntimeResult().failure(self._illegal())

    def get_attribute(self, name_token, context=None):
        return None, self._illegal()

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        return None, self._illegal()

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)

    def __repr__(self):
        return self.to_string([])
