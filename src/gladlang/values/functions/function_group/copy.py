"""Copies a FunctionGroup, including each of its overload variants."""


class FunctionGroupCopy:
    __slots__ = ()

    def copy(self):
        from gladlang.values.functions.function_group import FunctionGroup

        group_copy = FunctionGroup(self.name)

        group_copy._call_count = 0
        group_copy.visibility = self.visibility
        group_copy.is_static = self.is_static
        group_copy.defining_class = self.defining_class

        for argument_count, variant in self.functions.items():
            group_copy.functions[argument_count] = variant.copy()

        group_copy.set_position(self.position_start, self.position_end)
        group_copy.set_context(self.context)
        return group_copy
