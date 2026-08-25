"""Resolve and validate superclass inheritance for a CLASS node."""

from gladlang.core.errors import RuntimeError
from gladlang.parser.ast import VariableAccessNode
from gladlang.values.classes.class_ import Class


class InterpreterResolveSuperclasses:
    def _resolve_superclasses(self, result, class_node, context, class_name):
        superclasses = []

        if class_node.superclass_nodes:
            for super_node in class_node.superclass_nodes:
                if (
                    isinstance(super_node, VariableAccessNode)
                    and super_node.variable_name_token.value == class_name
                ):
                    result.failure(
                        RuntimeError(
                            super_node.position_start,
                            super_node.position_end,
                            f"Class '{class_name}' cannot inherit from itself",
                            context,
                        )
                    )
                    return None

                superclass = result.register(self.visit(super_node, context))
                if result.error:
                    return None

                if not isinstance(superclass, Class):
                    result.failure(
                        RuntimeError(
                            super_node.position_start,
                            super_node.position_end,
                            "A class can only inherit from another class",
                            context,
                        )
                    )
                    return None

                if superclass.name == class_name:
                    result.failure(
                        RuntimeError(
                            super_node.position_start,
                            super_node.position_end,
                            f"Class '{class_name}' cannot inherit from itself",
                            context,
                        )
                    )
                    return None

                superclasses.append(superclass)

        return superclasses
