"""Expected output fragments, part 2."""

OUTPUT_SUBSTRINGS_2 = {
    "test_calculator.glad": [
        "a = 10",
        "a + b = 30",
        "a * b = 200",
    ],
    "test_call_error.glad": [
        "Testing what happens when calling a non-function.",
        "Attempting to call x(5)...",
    ],
    "test_calling_context.glad": [
        "[PASS] A: method error propagates through outer function correctly",
        "[PASS] B: overloaded function error propagates through outer function correctly",
    ],
    "test_casting.glad": [
        "String as INT: 123",
        "Enter a number (e.g., 123.5):",
    ],
    "test_chaining.glad": [
        "Engine starts. Vroom!",
        "Car start status: Engine-OK",
    ],
    "test_closures.glad": [
        "add_five(3) = 8",
        "10 + 20 + 30 + 40 = 100 (expected: 100)",
    ],
    "test_comparisons.glad": [
        "[PASS] 5 == 5",
        "[PASS] 5 < 10",
    ],
    "test_comprehension.glad": [
        "Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]",
        "Evens: [2, 4, 6, 8, 10]",
    ],
    "test_comprehensive.glad": [
        "--- 1. Advanced Math ---\n8\n3\n1\n14",
        "--- 2. Comparisons ---",
    ],
    "test_comprehensive_oop.glad": [
        "[PASS] Public method works",
        "[PASS] Subclass accessed PROTECTED parent method",
    ],
    "test_destructuring.glad": [
        "x: 10",
        "Point: x=1, y=2",
    ],
    "test_dict.glad": [
        "Name: GladLang",
        "New Version: 1.1",
    ],
    "test_dict_comprehension.glad": [
        "Squares: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}",
        "=== ALL DICT COMP TESTS PASSED ===",
    ],
    "test_escapes.glad": [
        'Quote: "Hello"',
        "=== 2. Template String Escapes (Backticks) ===",
    ],
    "test_for_loop.glad": [
        "Item: apple",
        "Item: date",
    ],
    "test_functions.glad": [
        "Result of add: 15",
        "sum * 2 = 30",
    ],
    "test_inherited_this.glad": [
        "Fido says Woof!",
        "Result from get_name (should be Fido): Fido",
    ],
    "test_input.glad": [
        "Hello, Glad! Welcome to GladLang.",
        "You entered: Glad",
    ],
    "test_input_math.glad": [
        "Hello, Glad!",
        "The sum of 10 and 20 is: 30",
    ],
    "test_logic.glad": [
        "L3: z is 30 (TARGET REACHED!)",
        "Grade C (Correct)",
    ],
    "test_logic_ops.glad": [
        "a != b (TRUE): 1",
        "a >= 10 (TRUE): 1",
    ],
    "test_loops.glad": [
        "i = 5",
        "Loop 1 finished.",
    ],
    "test_module_error.glad": [
        "Attempting to import an unexported name...",
    ],
    "test_module_export_error.glad": [
        "Attempting to EXPORT from a non-module (the entry script)...",
    ],
    "test_modules.glad": [
        "add(10, 5) = 15",
        "calc.multiply(6, 7) = 42",
    ],
    "test_multiline.glad": [
        "Line 1: Hello",
        "Line 2: World",
    ],
    "test_name_error.glad": [
        "a = 10",
        "Attempting to access 'b'...",
    ],
    "test_nested_try.glad": [
        "Inner CATCH caught: Error from Inner",
        "Outer CATCH caught rethrown error: Error from Inner",
    ],
    "test_null_guards.glad": [
        "[PASS] 1a: 5 + NULL",
        "[PASS] 1f: 5 // NULL",
    ],
    "test_number_bases.glad": [
        "0xff (Expected: 255)   -> 255",
        "0xDEADBEEF (Expected: 3735928559) -> 3735928559",
    ],
    "test_numerics.glad": [
        "Literal -0 => 0",
        "neg_zero == 0 => 1",
    ],
}
