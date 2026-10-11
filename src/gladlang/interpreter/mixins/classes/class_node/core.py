"""Visitor for CLASS declarations: runs each build step in order."""

from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterClassNodeCore:
    def visit_ClassNode(self, class_node, context):
        result = RuntimeResult()

        class_name = class_node.class_name_token.value

        name_error = self._validate_class_name(result, class_node, context, class_name)
        if name_error is not None:
            return name_error

        superclasses = self._resolve_superclasses(
            result, class_node, context, class_name
        )

        if result.error:
            return result

        depth_error = self._check_inheritance_depth(
            result, class_node, context, superclasses
        )

        if depth_error is not None:
            return depth_error

        class_value, static_table, create_error = self._create_class_value(
            result, class_node, context, class_name, superclasses
        )

        if create_error is not None:
            return create_error

        static_error = self._evaluate_static_fields(
            result, class_node, context, class_name, class_value, static_table
        )

        if static_error is not None:
            return static_error

        methods, build_error = self._build_methods(
            result, class_node, context, class_value
        )

        if build_error is not None:
            return build_error

        method_conflict = self._check_methods_vs_static_fields(
            result, class_node, context, class_name, class_value, static_table, methods
        )

        if method_conflict is not None:
            return method_conflict

        field_conflict = self._check_static_fields_vs_methods(
            result, class_node, context, class_name, class_value, static_table, methods
        )

        if field_conflict is not None:
            return field_conflict

        self._register_class(context, class_name, class_value, methods)

        return result.success(class_value)
