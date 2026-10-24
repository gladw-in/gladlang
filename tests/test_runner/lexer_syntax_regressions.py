"""Regression cases that must be driven from Python rather than as standalone .glad files."""

REGRESSION_CASES = [
    (
        "escape_high_surrogate",
        'PRINTLN "\\uD800"',
        "A \\u escape for a UTF-16 high surrogate (0xD800-0xDBFF) must "
        "be rejected while lexing the string literal.",
    ),
    (
        "escape_low_surrogate",
        'PRINTLN "\\uDFFF"',
        "A \\u escape for a UTF-16 low surrogate (0xDC00-0xDFFF) must "
        "be rejected while lexing the string literal.",
    ),
    (
        "number_base_hex_leading_underscore",
        "PRINTLN 0x_FF",
        "A hex literal cannot start its digit run with an underscore "
        "right after the 0x prefix.",
    ),
    (
        "number_base_hex_trailing_underscore",
        "PRINTLN 0xFF_",
        "A hex literal cannot end with a trailing underscore.",
    ),
    (
        "number_base_hex_double_underscore",
        "PRINTLN 0xFF__FF",
        "A hex literal cannot contain two consecutive underscores " "between digits.",
    ),
    (
        "number_base_bin_leading_underscore",
        "PRINTLN 0b_1010",
        "A binary literal cannot start its digit run with an "
        "underscore right after the 0b prefix.",
    ),
    (
        "number_base_bin_trailing_underscore",
        "PRINTLN 0b1010_",
        "A binary literal cannot end with a trailing underscore.",
    ),
    (
        "number_base_oct_leading_underscore",
        "PRINTLN 0o_77",
        "An octal literal cannot start its digit run with an "
        "underscore right after the 0o prefix.",
    ),
    (
        "number_base_oct_trailing_underscore",
        "PRINTLN 0o77_",
        "An octal literal cannot end with a trailing underscore.",
    ),
    (
        "numeric_positive_infinity",
        "PRINTLN 1e999",
        "A float literal that overflows to +inf must be rejected at "
        "lex time, not silently turned into an `inf` value.",
    ),
    (
        "numeric_negative_infinity",
        "PRINTLN -1e999",
        "A float literal that overflows to -inf must be rejected at "
        "lex time, not silently turned into a `-inf` value.",
    ),
    (
        "numeric_decimal_underscore_after_dot",
        "PRINTLN 1._2",
        "An underscore cannot immediately follow the decimal point.",
    ),
    (
        "numeric_decimal_underscore_before_dot",
        "PRINTLN 1_.2",
        "An underscore cannot immediately precede the decimal point.",
    ),
    (
        "numeric_decimal_trailing_underscore",
        "PRINTLN 1.2_",
        "A decimal literal cannot end with a trailing underscore.",
    ),
    (
        "template_unterminated",
        "LET bad_template = `unterminated",
        "An unterminated backtick template string must be rejected " "while parsing.",
    ),
    (
        "overload_inherited_private_visibility",
        """
CLASS PrivateBase
    PRIVATE FUNC secret(a)
        RETURN 100
    ENDFUNC
ENDCLASS

CLASS PrivateChild INHERITS PrivateBase
    PUBLIC FUNC secret(a, b)
        RETURN 200
    ENDFUNC
ENDCLASS
""",
        "A child class cannot add a different-arity overload of a "
        "PRIVATE inherited method; merging the overload set would "
        "leak the parent's private variant. Rejected when the class "
        "is built.",
    ),
    (
        "overload_inherited_protected_visibility",
        """
CLASS ProtectedBase
    PROTECTED FUNC protected_method(a)
        RETURN 300
    ENDFUNC
ENDCLASS

CLASS ProtectedChild INHERITS ProtectedBase
    PUBLIC FUNC protected_method(a, b)
        RETURN 400
    ENDFUNC
ENDCLASS
""",
        "A child class cannot add a different-arity overload of a "
        "PROTECTED inherited method; merging the overload set would "
        "leak the parent's protected variant. Rejected when the class "
        "is built.",
    ),
]

REGRESSION_EXPECTED_ERRORS = {
    "escape_high_surrogate": "surrogate code point",
    "escape_low_surrogate": "surrogate code point",
    "number_base_hex_leading_underscore": "Invalid hex literal",
    "number_base_hex_trailing_underscore": "Invalid hex literal",
    "number_base_hex_double_underscore": "Invalid hex literal",
    "number_base_bin_leading_underscore": "Invalid binary literal",
    "number_base_bin_trailing_underscore": "Invalid binary literal",
    "number_base_oct_leading_underscore": "Invalid octal literal",
    "number_base_oct_trailing_underscore": "Invalid octal literal",
    "numeric_positive_infinity": "Floating-point literal is not finite",
    "numeric_negative_infinity": "Floating-point literal is not finite",
    "numeric_decimal_underscore_after_dot": "Invalid numeric literal",
    "numeric_decimal_underscore_before_dot": "Invalid numeric literal",
    "numeric_decimal_trailing_underscore": "Invalid numeric literal",
    "template_unterminated": "Unterminated template string",
    "overload_inherited_private_visibility": "All overloads of 'secret' must have the same visibility",
    "overload_inherited_protected_visibility": "All overloads of 'protected_method' must have the same visibility",
}
