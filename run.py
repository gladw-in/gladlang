import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gladlang.__main__ import main

if __name__ == "__main__":
    main()
