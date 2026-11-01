"""Entry point that runs the GladLang test suite."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tests"))

from test_runner import main

if __name__ == "__main__":
    main()
