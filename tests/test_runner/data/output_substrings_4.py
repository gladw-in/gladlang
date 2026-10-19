"""Expected output fragments, part 4."""

OUTPUT_SUBSTRINGS_4 = {
    "test_module_import_errors.glad": [
        "PASS: empty path -> Import path must be a non-empty string",
        "PASS: importing twice -> Variable 'PI' is already defined",
        "PASS: nothing from the failed import is defined",
    ],
    "test_module_values.glad": [
        "PASS: constant member",
        "PASS: module is an Object",
        "PASS: text form",
        "PASS: LEN of a module -> LEN is not supported for type 'Module'",
    ],
    "test_delay_errors.glad": [
        "PASS: no argument -> DELAY expects one argument (seconds)",
        "PASS: negative delay -> DELAY argument must not be negative",
        "PASS: a delay of zero returns immediately",
    ],
    "test_switch_forms.glad": [
        "PASS: an empty switch does nothing",
        "PASS: cases-only switch runs a matching case",
        "PASS: string cases",
    ],
}
