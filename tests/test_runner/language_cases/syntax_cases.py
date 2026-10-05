"""Parser error message cases."""

EXPECTED_EXPRESSION = (
    "Invalid Syntax: Expected int, float, string, identifier, '+', '-', '++', '--'"
)


SYNTAX_CASES = [
    (
        "param_reserved_word",
        "FUNC f(IF)\nRETURN 1\nENDFUNC",
        "Invalid Syntax: Expected identifier",
    ),
    (
        "param_this",
        "FUNC f(THIS)\nRETURN 1\nENDFUNC",
        "Invalid Syntax: 'THIS' is reserved and cannot be used as a parameter name",
    ),
    (
        "second_param_this",
        "FUNC f(a, THIS)\nRETURN 1\nENDFUNC",
        "Invalid Syntax: 'THIS' is reserved and cannot be used as a parameter name",
    ),
    (
        "second_param_number",
        "FUNC f(a, 1)\nRETURN 1\nENDFUNC",
        "Invalid Syntax: Expected identifier",
    ),
    (
        "missing_rparen_params",
        "FUNC f(a, b\nRETURN 1\nENDFUNC",
        "Invalid Syntax: Expected ',' or ')'",
    ),
    (
        "missing_comma_params",
        "FUNC f(a b)\nRETURN 1\nENDFUNC",
        "Invalid Syntax: Expected ',' or ')'",
    ),
    (
        "for_no_variable",
        "FOR IN [1]\nENDFOR",
        "Invalid Syntax: Expected identifier or '[...]' for loop variable",
    ),
    ("for_missing_in", "FOR x [1]\nENDFOR", "Invalid Syntax: Expected 'IN'"),
    (
        "for_missing_endfor",
        "FOR x IN [1]\nPRINTLN x",
        "Invalid Syntax: Expected 'ENDFOR'",
    ),
    (
        "final_non_static_field",
        "CLASS A\n  FINAL x = 1\nENDCLASS",
        "Invalid Syntax: Class-level constants must be declared with STATIC FINAL",
    ),
    (
        "class_field_not_assignment",
        "CLASS A\n  PUBLIC 5\nENDCLASS",
        "Invalid Syntax: Expected 'FUNC', 'LET', 'FINAL' or 'STATIC' inside class body",
    ),
    (
        "visibility_on_expression",
        "PRIVATE 5",
        "Invalid Syntax: Visibility modifiers can only be used with variable or attribute assignments",
    ),
    (
        "visibility_on_call",
        "PUBLIC foo()",
        "Invalid Syntax: Visibility modifiers can only be used with variable or attribute assignments",
    ),
    ("print_missing_rparen", "PRINTLN(1, 2", "Invalid Syntax: Expected ')'"),
    ("print_trailing_comma", "PRINTLN(1,)", EXPECTED_EXPRESSION),
    (
        "template_unterminated_interpolation",
        "PRINTLN `a ${1 + `",
        "Invalid Syntax: Unterminated template string",
    ),
    (
        "template_unclosed_brace",
        "PRINTLN `a ${1 + 2",
        "Invalid Syntax: Unterminated template string",
    ),
    ("template_bad_expression", "PRINTLN `a ${1 + } b`", EXPECTED_EXPRESSION),
    ("else_without_if", "ELSE\nPRINTLN 1", EXPECTED_EXPRESSION),
    ("endif_without_if", "ENDIF", "Invalid Syntax: Unexpected 'ENDIF'"),
    ("catch_without_try", "CATCH e\nPRINTLN 1", EXPECTED_EXPRESSION),
    (
        "unterminated_string",
        'PRINTLN "abc',
        "Invalid Syntax: Unterminated string literal",
    ),
    ("illegal_character", "PRINTLN 1 @ 2", "Illegal Character: '@'"),
    (
        "class_without_end",
        "CLASS A\n PUBLIC FUNC f()\n RETURN 1\n ENDFUNC",
        "Invalid Syntax: Expected 'ENDCLASS'",
    ),
    ("switch_case_without_value", "SWITCH 1\nCASE\nENDSWITCH", EXPECTED_EXPRESSION),
    (
        "cfor_missing_first_semicolon",
        "FOR (LET i = 0 i < 2; i++)\n PRINTLN i\nENDFOR",
        "Invalid Syntax: Expected ';'",
    ),
    (
        "cfor_missing_second_semicolon",
        "FOR (LET i = 0; i < 2 i++)\n PRINTLN i\nENDFOR",
        "Invalid Syntax: Expected ';'",
    ),
    (
        "cfor_missing_rparen",
        "FOR (LET i = 0; i < 2; i++\n PRINTLN i\nENDFOR",
        "Invalid Syntax: Expected ')'",
    ),
    (
        "cfor_missing_endfor",
        "FOR (LET i = 0; i < 2; i++)\n PRINTLN i",
        "Invalid Syntax: Expected 'ENDFOR'",
    ),
    (
        "static_constructor",
        "CLASS A\n STATIC FUNC A()\n RETURN 1\n ENDFUNC\nENDCLASS",
        "Invalid Syntax: Constructor 'A' cannot be STATIC",
    ),
    (
        "anonymous_method",
        "CLASS A\n FUNC ()\n RETURN 1\n ENDFUNC\nENDCLASS",
        "Invalid Syntax: Anonymous functions are not allowed inside a class body, methods must have a name",
    ),
    (
        "method_bad_parameters",
        "CLASS A\n FUNC f(\n RETURN 1\n ENDFUNC\nENDCLASS",
        "Invalid Syntax: Expected identifier",
    ),
    (
        "method_missing_enddef",
        "CLASS A\n FUNC f()\n RETURN 1\nENDCLASS",
        EXPECTED_EXPRESSION,
    ),
    ("break_outside_loop", "BREAK", "Invalid Syntax: 'BREAK' outside of loop"),
    (
        "return_outside_function",
        "RETURN 1",
        "Invalid Syntax: 'RETURN' outside of function",
    ),
]
