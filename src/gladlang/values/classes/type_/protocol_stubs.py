"""Default illegal-operation stubs: Type can't be called, indexed, or mutated."""

from gladlang.core.errors import RuntimeError


class TypeProtocolStubs:
    __slots__ = ()

    def execute(self, arguments, interpreter=None, calling_context=None):
        from gladlang.runtime.runtime_result import RuntimeResult

        return RuntimeResult().failure(self._illegal())

    def get_attribute(self, name_token, context=None):
        return None, self._illegal()

    def set_attribute(
        self, name_token, value, context=None, visibility=None, as_final=False
    ):
        return None, self._illegal()

    def get_element_at(self, index):
        return None, self._illegal()

    def set_element_at(self, index, value):
        return None, self._illegal()

    def notted(self):
        return None, self._illegal()

    def _illegal(self, other=None):
        if not other:
            other = self

        return RuntimeError(
            self.position_start, other.position_end, "Illegal operation", self.context
        )

    def illegal_operation(self, other=None):
        return self._illegal(other)
