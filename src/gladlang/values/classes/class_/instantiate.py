"""Instantiate a class: build instance and run constructor."""

from gladlang.core.constants import GL_IDENTIFIER
from gladlang.core.errors import RuntimeError
from gladlang.lexer.token import Token
from gladlang.runtime.runtime_result import RuntimeResult


class ClassInstantiate:
    __slots__ = ()

    def instantiate(
        self,
        arguments,
        context=None,
        interpreter=None,
        call_position_start=None,
        call_position_end=None,
        calling_context=None,
    ):
        result = RuntimeResult()

        from gladlang.values.classes.instance_ import Instance

        instance = Instance(self)
        constructor_name = None

        for current_class in self.mro:
            if current_class.name in current_class.methods:
                constructor_name = current_class.name
                break

        if constructor_name:
            fake_token = Token(
                GL_IDENTIFIER, constructor_name, self.position_start, self.position_end
            )

            init_method, error = self.get_attribute(
                fake_token, context, allow_instance=True
            )

            if error:
                return result.failure(error)

            bound_init = init_method.copy().bind_to_instance(instance)
            if call_position_start is not None:
                bound_init.set_position(call_position_start, call_position_end)

            result.register(bound_init.execute(arguments, interpreter, calling_context))
            if result.error:
                return result

        else:
            if len(arguments) > 0:
                return result.failure(
                    RuntimeError(
                        call_position_start or self.position_start,
                        call_position_end or self.position_end,
                        f"'{self.name}' does not have a constructor that accepts arguments",
                        context or self.context,
                    )
                )

        return result.success(instance)
