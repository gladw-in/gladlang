"""Check that the inheritance chain is not deeper than the allowed limit."""

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings


class InterpreterClassNodeCheckDepth:
    def _check_inheritance_depth(self, result, class_node, context, superclasses):
        for superclass in superclasses:
            if len(superclass.mro) >= Settings.MAX_INHERITANCE_DEPTH:
                return result.failure(
                    RuntimeError(
                        class_node.position_start,
                        class_node.position_end,
                        f"Inheritance chain too deep (exceeds limit of {Settings.MAX_INHERITANCE_DEPTH})",
                        context,
                    )
                )

        return None
