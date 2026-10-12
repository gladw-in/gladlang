"""Check that all overloads of one method share the same visibility and static mode."""

from gladlang.core.errors import RuntimeError


class InterpreterBuildMethodsValidateOverloads:
    def _validate_overload_variants(self, result, method_name, variants, context):
        reference_variant = variants[0]

        expected_visibility = getattr(
            reference_variant,
            "visibility",
            "PUBLIC",
        )

        expected_static = getattr(
            reference_variant,
            "is_static",
            False,
        )

        for variant in variants[1:]:
            variant_visibility = getattr(
                variant,
                "visibility",
                "PUBLIC",
            )

            if variant_visibility != expected_visibility:
                return result.failure(
                    RuntimeError(
                        variant.position_start,
                        variant.position_end,
                        f"All overloads of '{method_name}' must have "
                        "the same visibility",
                        context,
                    )
                )

            variant_static = getattr(
                variant,
                "is_static",
                False,
            )

            if variant_static != expected_static:
                return result.failure(
                    RuntimeError(
                        variant.position_start,
                        variant.position_end,
                        f"All overloads of '{method_name}' must have "
                        "the same static/instance mode",
                        context,
                    )
                )

        return None
