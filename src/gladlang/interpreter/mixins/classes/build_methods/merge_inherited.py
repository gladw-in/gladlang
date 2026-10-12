"""Add methods inherited from parent classes, merging overloads with the child's."""

from gladlang.values.functions.function_group import FunctionGroup


def _as_variants(candidate):
    if isinstance(candidate, FunctionGroup):
        return dict(candidate.functions)

    return {len(candidate.argument_names): candidate}


class InterpreterBuildMethodsMergeInherited:
    def _merge_inherited_methods(self, result, methods, context, class_value):
        for ancestor in class_value.mro[1:]:
            for method_name, ancestor_method in ancestor.methods.items():
                if method_name not in methods:
                    methods[method_name] = ancestor_method
                    continue

                child_method = methods[method_name]

                ancestor_variants = _as_variants(ancestor_method)
                child_variants = _as_variants(child_method)

                merged_variants = dict(ancestor_variants)
                merged_variants.update(child_variants)

                if len(merged_variants) == 1:
                    methods[method_name] = next(iter(merged_variants.values()))
                    continue

                variants = list(merged_variants.values())
                reference_variant = variants[0]

                error = self._validate_overload_variants(
                    result, method_name, variants, context
                )

                if error is not None:
                    return error

                merged_group = FunctionGroup(method_name)
                merged_group.functions = merged_variants
                merged_group.visibility = getattr(
                    reference_variant,
                    "visibility",
                    "PUBLIC",
                )

                merged_group.is_static = getattr(
                    reference_variant,
                    "is_static",
                    False,
                )

                merged_group.defining_class = getattr(
                    reference_variant,
                    "defining_class",
                    None,
                )

                methods[method_name] = merged_group

        return None
