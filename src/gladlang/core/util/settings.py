"""Central configuration for GladLang – all system limits and constants."""

import sys

from gladlang.version import __version__


class Settings:
    THREADING_ENABLED = True

    MAX_NESTING = 200
    MAX_TOKENS = 200_000
    MAX_TERNARY_CHAIN = 500

    MAX_TRACEBACK_FRAMES = 20

    MAX_TEMPLATE_DEPTH = 10
    MAX_INTERPOLATION_SIZE = 10000

    MAX_LIST_SIZE = 1_000_000
    MAX_DICT_SIZE = 1_000_000
    MAX_STRING_SIZE = 10_000_000
    MAX_INT_BITS = 100_000

    MAX_TOTAL_RECURSION = 10000
    PYTHON_RECURSION_LIMIT = 20_000

    MAX_INSTRUCTIONS = int(sys.maxsize)

    MAX_MEMORY_MB = 512
    MAX_SOURCE_BYTES = 1_000_000
    MAX_REPL_BUFFER = 100_000

    MAX_INT_STR_DIGITS = 50_000
    MAX_CONTEXT_DEPTH = 2000
    MAX_INHERITANCE_DEPTH = 500

    MAX_EXPONENT = 1000
    MAX_BASE_BITS_FOR_EXPONENT = 1000

    MAX_DELAY_SECONDS = 60
    MAX_PRINTF_PRECISION = 100

    BITWISE_MASK = 0xFFFFFFFF
    BITWISE_SIGN_BIT = 0x80000000
    BITWISE_COMPLEMENT = 0x100000000
    BITWISE_MAX_SHIFT = 32

    WATCHDOG_SLEEP_INTERVAL = 0.05

    VERSION = str(__version__)

    TITLE = "GladLang"

    HELP = """
Usage: gladlang [command] [filename/code] [args...]

Commands:
  <no arguments>           Start the interactive GladLang shell.
  [filename.glad]          Execute a GladLang script file.
  ["code string"]          Execute inline GladLang code directly.
  [filename.glad] [args]   Execute script and pass args to INPUT().
  ["code string"] [args]   Execute inline code and pass args to INPUT().
  -h, --help               Show this help message and exit.
  -v, --version            Show the interpreter version and exit.
"""
