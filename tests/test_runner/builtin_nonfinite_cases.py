"""Runtime guards for non-finite numbers in built-ins."""

NONFINITE_CASES = [
    (
        "printf_inf",
        "TRY\n"
        '    PRINTF("%d\\n", INF_VALUE)\n'
        '    PRINTLN "FAIL: should have caught overflow"\n'
        "CATCH e\n"
        '    PRINTLN "Caught expected error (PRINTF inf): ", e\n'
        "ENDTRY\n",
        "Caught expected error (PRINTF inf):  Cannot format non-finite value inf as integer for '%d'\n",
    ),
    (
        "random_range_inf",
        "TRY\n"
        "    RANDOM_RANGE(0, INF_VALUE)\n"
        '    PRINTLN "FAIL: should have caught overflow"\n'
        "CATCH e\n"
        '    PRINTLN "Caught expected error (RANDOM_RANGE inf): ", e\n'
        "ENDTRY\n",
        "Caught expected error (RANDOM_RANGE inf):  Arguments to RANDOM_RANGE must be finite numbers (not inf or nan)\n",
    ),
    (
        "printf_inf_with_precision",
        "TRY\n"
        '    PRINTF("%.2f\\n", INF_VALUE)\n'
        '    PRINTLN "inf with precision handled without crashing"\n'
        "CATCH e\n"
        '    PRINTLN "FAIL: should not have raised for inf with precision: ", e\n'
        "ENDTRY\n",
        "inf\ninf with precision handled without crashing\n",
    ),
]
