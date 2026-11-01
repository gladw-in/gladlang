# Golden-output fixtures

These fixtures provide whole-program output and complete diagnostic baselines for the GladLang test runner.

- `.stdout` files are compared as complete strings. Only line endings are normalized (`CRLF` and bare `CR` become `LF`); leading/trailing spaces, blank lines, punctuation, and final newline presence remain significant.
- `.error` files contain the complete expected runtime/parse diagnostic. The repository root is normalized to `$REPO` so diagnostics do not depend on the checkout directory.
- `{{INTEGER}}` and `{{NUMBER}}` are narrowly-scoped placeholders used only by `test_builtins.glad` for values that intentionally vary between runs (clock values, random values, and measured delay). All surrounding text and whitespace is still exact.
- `inline_errors.json` and `token_limit_errors.json` store complete diagnostics for direct Python-driven regression cases.

These are fixed regression fixtures. Do not regenerate them automatically during ordinary test runs; update them intentionally when behavior changes and review the diff.
