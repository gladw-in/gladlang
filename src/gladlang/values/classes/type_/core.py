"""Core Type machinery: slots, construction, and identity/copy/repr."""


class TypeCore:
    __slots__ = ()

    def __init__(self, name):
        self.name = name
        self.position_start = None
        self.position_end = None
        self.context = None

    def set_position(self, position_start=None, position_end=None):
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def is_true(self):
        return True

    def copy(self):
        from gladlang.values.classes.type_ import Type

        return (
            Type(self.name)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

    def __repr__(self):
        return f"<type {self.name}>"
