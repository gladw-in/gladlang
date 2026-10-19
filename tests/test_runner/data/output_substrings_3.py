"""Expected output fragments, part 3."""

OUTPUT_SUBSTRINGS_3 = {
    "test_oop.glad": [
        "Ref Equality (True): 1",
        "Buddy says: Woof!",
    ],
    "test_polymorphism.glad": [
        "My name is Buddy. I am a pet and I say:",
        "Meow!",
    ],
    "test_runtime_error.glad": [
        "This script will test for a division by zero error.",
        "Attempting to calculate a / b...",
    ],
    "test_slice.glad": [
        "[0, 1, 2]",
        "Positive slice: nums[1:4] = [20, 30, 40] (expected: [20,30,40])",
    ],
    "test_super_instanceof.glad": [
        "Animal Constructor",
        "Buddy says Woof!",
    ],
    "test_switch.glad": [
        "Value is 10",
        "Matched 5 + 5",
    ],
    "test_template.glad": [
        "Hello, GladLang!",
        "Math: 5 + 5 = 10",
    ],
    "test_ternary.glad": [
        "TRUE ? 10 : 20   => 10",
        "50 < 100 ? 'Less' : 'More' => Less",
    ],
    "test_this.glad": [
        "Initial count: 0",
        "Count after second add_two: 4",
    ],
    "test_traceback_all.glad": [
        "[PASS] Test 1a: THROW fires with correct message",
        "[PASS] Test 2: error propagates correctly through TRY/CATCH/RETHROW chain",
    ],
    "test_try_catch.glad": [
        "Caught system error: Division by zero",
        "Finally 1 executed.",
    ],
    "test_valid_float_literals.glad": [
        "3.14\n1000.23\n2e-10\n6.022e+23",
    ],
    "test_short_circuit.glad": [
        "PASS: FALSE AND x -> RHS not evaluated",
        "PASS: TRUE OR x -> RHS not evaluated",
        "PASS: 0 AND (1/0) -> falsy",
        "PASS: 0 OR (1/0) raised: Division by zero",
    ],
    "test_finally_errors.glad": [
        "PASS: FINALLY error replaces TRY error",
        "PASS: FINALLY error beats RETURN",
        "PASS: RETURN value preserved by clean FINALLY",
    ],
    "test_size_limits.glad": [
        "PASS: list of exactly 1,000,000 is allowed",
        "Caught: List repetition result (1000001) exceeds maximum allowed size (1000000)",
        "Caught: String concatenation result (10,000,001 chars) exceeds maximum allowed size (10,000,000 chars)",
    ],
    "test_instanceof_matrix.glad": [
        "PASS: int",
        "PASS: bound method",
        "PASS: subclass instance of parent",
        "PASS: enum INSTANCEOF number -> Right operand of INSTANCEOF must be a Class or Type",
    ],
    "test_illegal_operations.glad": [
        "PASS: type Number: v + 1 -> Illegal operation",
        "PASS: enum member: v == 1 is allowed",
        "PASS: class A: v.x = 1 is allowed",
        "PASS: bound method: v++ -> Operand must be a number",
    ],
    "test_deep_copy.glad": [
        "PASS: list cycle is preserved in the copy",
        "PASS: dict cycle is preserved in the copy",
        "PASS: bound method still callable",
        "PASS: three levels deep are independent",
    ],
    "test_enum_operators.glad": [
        "PASS: member == itself",
        "PASS: enum != another enum",
        "PASS: missing case -> Enum 'Colors' has no case 'MISSING'",
        "PASS: LEN of an enum -> LEN is not supported for type 'Enum'",
    ],
    "test_compound_targets.glad": [
        "PASS: attribute +=",
        "PASS: element >>=",
        "PASS: private attribute += through a method",
        "PASS: index out of range -> List index 99 out of bounds",
    ],
    "test_destructuring_errors.glad": [
        "PASS: swap",
        "PASS: too few values -> Cannot unpack 1 value(s) into 2 variable(s)",
        "PASS: constant -> Cannot reassign constant 'k'",
        "PASS: shadowing a constant inside a function -> Cannot shadow constant 'k'",
    ],
    "test_null_ordering.glad": [
        "PASS: NULL < 5 -> Illegal operation",
        "PASS: NULL == instance is false",
        "PASS: NOT NULL",
    ],
    "test_super_rules.glad": [
        "PASS: SUPER() with no arguments is accepted",
        "PASS: subclass may call a protected parent constructor",
    ],
    "test_visibility_set_rules.glad": [
        "PASS: public static can be set",
        "PASS: protected static from outside",
        "PASS: private value is never overwritten from outside",
    ],
    "test_number_error_branches.glad": [
        "PASS: v + v",
        "PASS: float + float",
        "PASS: shifting by 32 or more clears the value",
    ],
    "test_print_forms.glad": [
        "no newline, continued",
        "1 a 3",
        'list: [1, 2] dict: {"k": 1}',
    ],
}
