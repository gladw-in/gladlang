"""Regression cases for token and literal size limits."""

TOKEN_LIMIT_CASES = [
    ("trailing_whitespace_at_limit", "LET a = 1 ", 4, 4, None),
    (
        "ordinary_source_over_limit",
        "LET a = 1 +",
        4,
        None,
        "Source produces too many tokens",
    ),
    ("template_at_limit", "`abc`", 3, 3, None),
    ("template_over_limit", "`abc`", 2, None, "Source produces too many tokens"),
    (
        "prefix_template_total_over_limit",
        "LET a = 1 `abc`",
        6,
        None,
        "Source produces too many tokens",
    ),
    (
        "template_interpolation_at_limit",
        "`value=${1}`",
        10,
        10,
        None,
    ),
    (
        "template_interpolation_over_limit",
        "`value=${1}`",
        9,
        None,
        "Source produces too many tokens",
    ),
    (
        "prefix_interpolation_total_at_limit",
        "LET a = 1 `value=${1}`",
        14,
        14,
        None,
    ),
    (
        "prefix_interpolation_total_over_limit",
        "LET a = 1 `value=${1}`",
        13,
        None,
        "Source produces too many tokens",
    ),
]
