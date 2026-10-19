"""Expected output fragments, part 1."""

OUTPUT_SUBSTRINGS_1 = {
    "test_precedence.glad": [
        "1 + 2 * 3 = 7",
        "(1 + 2) * 3 = 9",
        "10 - 4 / 2 = 8.0",
        "s1 < s2 (TRUE): 1",
        "s1 > s2 (FALSE): 0",
    ],
    "test_overloading.glad": [
        "add(10, 20) = 30",
        "add(10, 20, 30) = 60",
        "c.calc(10) = 20",
        "c.calc(10, 5) = 50",
        "c.calc(1, 2, 3) = 6",
        "Vector() = [0, 0]",
        "Vector(5, 10) = [5, 10]",
        "Same-arity override result: 600",
        "PASS: static/instance overload mismatch rejected",
        "Inherited overload: 10",
        "Child overload: 20",
    ],
    "test_lists.glad": [
        'Initial list: [1, "hello", 6, 1]',
        'New list: [1, "world", 6, 1]',
        "PASS: Fractional list index rejected",
        "PASS: Fractional slice start rejected",
        "PASS: Fractional slice end rejected",
        "PASS: Fractional repetition count rejected",
    ],
    "test_static.glad": [
        "Initial inherited static value: 1",
        "Updated inherited static value: 2",
        "SUCCESS: Static field/method collision rejected:",
    ],
    "test_assignments.glad": [
        "SUCCESS: Addition Verified",
        "SUCCESS: Subtraction Verified",
        "SUCCESS: Multiplication Verified",
        "SUCCESS: Division Verified",
        "SUCCESS: Modulo Verified",
        "PASS: Add Zero Identity verified",
        "SUCCESS: Caught exponent too large ->",
    ],
    "test_bitwise.glad": [
        "PASS: & binds tighter than == (verified, not coincidental)",
        "PASS: fractional AND rejected",
        "PASS: fractional OR rejected",
        "PASS: fractional XOR rejected",
        "PASS: fractional NOT rejected",
        "PASS: fractional shift rejected",
    ],
    "test_builtins.glad": [
        "RANDOM_RANGE range OK",
        "DELAY duration seems plausible",
        "All tests completed successfully.",
    ],
    "test_enums.glad": [
        "PASS: Same enum member compares equal",
        "PASS: Different enum members compare not equal",
        "PASS: RED.value = 0",
        "PASS: Enum member is truthy",
        "ALL TESTS COMPLETED",
    ],
    "test_final.glad": [
        "SUCCESS: Global variable updated correctly.",
        "SUCCESS: Nested function cannot shadow FINAL:",
        "SUCCESS: Nested function parameter cannot shadow FINAL:",
        "SUCCESS: Nested class cannot shadow FINAL:",
        "SUCCESS: Nested enum cannot shadow FINAL:",
    ],
    "test_increment.glad": [
        "SUCCESS: Caught expected error ->",
    ],
    "test_inheritance.glad": [
        "SUCCESS: Self-inheritance error caught ->",
    ],
    "test_null_inequality.glad": [
        "PASS: IF NULL != FALSE executed (correct)",
        "PASS: IF NULL == FALSE skipped (correct)",
    ],
    "test_recursion.glad": [
        "=== All tests completed ===",
    ],
    "test_strings.glad": [
        "PASS: Fractional string index rejected",
        "PASS: Fractional string repetition rejected",
    ],
    "test_visibility_comprehensive.glad": [
        "PASS: error message identical regardless of cache order",
    ],
    "test_all_modifiers.glad": [
        "SUCCESS: Caught protected attribute error ->",
        "SUCCESS: Caught protected method error ->",
        "SUCCESS: Caught private attribute error ->",
        "SUCCESS: Caught private method error ->",
        "SUCCESS: Caught private static attribute error ->",
    ],
    "test.glad": [
        "Hi, I am Alex",
        "Hi, I am Bob",
    ],
    "test_access_modifiers.glad": [
        "Public Variable: 10",
        "CAUGHT ERROR: Cannot access private method 'secret' via Class",
    ],
    "test_advanced_oop.glad": [
        "Hello, Alex!",
        "Hi, Bob!",
    ],
    "test_anonymous.glad": [
        "double(5) = 10",
        "IIFE (6, 7) Result: 42",
    ],
    "test_arg_error.glad": [
        "Calling add(10, 5, 20)...",
    ],
    "test_attr_error.glad": [
        "Person's name: Alex",
        "Attempting to access 'p.age'...",
    ],
    "test_bool.glad": [
        "BOOL(123) = 1",
        'BOOL("") = 0',
    ],
}
