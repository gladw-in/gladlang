"""Binds a FunctionGroup to an instance, producing a BoundMethod."""


class FunctionGroupBindToInstance:
    __slots__ = ()

    def bind_to_instance(self, instance):
        from gladlang.values.functions.bound_method import BoundMethod

        return BoundMethod(self.name, self, instance)
