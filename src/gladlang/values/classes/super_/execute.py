"""Execute SUPER() constructor call from within a matching constructor."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class SuperExecute:
    __slots__ = ()

    def execute(self, arguments, interpreter, calling_context=None):
        result = RuntimeResult()

        in_constructor = (
            calling_context is not None
            and self.context is not None
            and self.context.active_class is not None
            and calling_context.display_name == self.context.active_class.name
        )

        if not in_constructor:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "'SUPER()' can only be called as a constructor call from within "
                    "a constructor. To call a parent method use 'SUPER.<method>(...)' instead.",
                    self.context,
                )
            )

        mro = self.instance.class_reference.mro

        try:
            start_index = mro.index(self.start_class) + 1
        except ValueError:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "Current class not found in MRO",
                    self.context,
                )
            )

        constructor_method, error = self._find_super_constructor(mro, start_index)
        if error:
            return result.failure(error)

        if constructor_method:
            bound_method = constructor_method.copy().bind_to_instance(self.instance)
            bound_method.set_position(self.position_start, self.position_end)
            execute_result = bound_method.execute(
                arguments, interpreter, calling_context
            )

            if execute_result.error:
                return execute_result

            return RuntimeResult().success(Number.null.copy())

        if len(arguments) > 0:
            return result.failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    "No constructor found in superclasses",
                    self.context,
                )
            )

        return result.success(Number.null.copy())
