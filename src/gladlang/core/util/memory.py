"""Memory limit management – sets process memory limits via resource or watchdog thread."""

import os
import sys
import threading
import time

try:
    import resource
except ImportError:
    resource = None

try:
    import psutil
except ImportError:
    psutil = None

from gladlang.core.util.settings import Settings


def start_memory_watchdog(max_mb):
    if psutil is None:
        return

    def watch():
        process = psutil.Process(os.getpid())
        memory_limit_bytes = max_mb * 1024 * 1024

        while True:
            if process.memory_info().rss > memory_limit_bytes:
                sys.stderr.write("System Error: Memory Limit Exceeded\n")
                os._exit(1)

            time.sleep(Settings.WATCHDOG_SLEEP_INTERVAL)

    watchdog_thread = threading.Thread(target=watch, daemon=True)
    watchdog_thread.start()


def set_memory_limit(max_mb):
    if resource is not None:
        try:
            soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
            limit_bytes = max_mb * 1024 * 1024
            new_soft_limit = (
                min(limit_bytes, hard_limit)
                if hard_limit != resource.RLIM_INFINITY
                else limit_bytes
            )

            resource.setrlimit(resource.RLIMIT_AS, (new_soft_limit, hard_limit))
        except Exception as exception:
            sys.stderr.write(f"Warning: Could not set memory limit: {exception}\n")
    else:
        start_memory_watchdog(max_mb)
