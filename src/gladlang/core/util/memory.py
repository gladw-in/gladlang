"""Memory limit management – sets the process memory limit via the resource module where available."""

import sys

try:
    import resource
except ImportError:
    resource = None


def set_memory_limit(max_megabytes):
    if resource is None:
        return

    try:
        _, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
        limit_bytes = max_megabytes * 1024 * 1024
        new_soft_limit = (
            min(limit_bytes, hard_limit)
            if hard_limit != resource.RLIM_INFINITY
            else limit_bytes
        )

        resource.setrlimit(resource.RLIMIT_AS, (new_soft_limit, hard_limit))
    except Exception as exception:
        sys.stderr.write(f"Warning: Could not set memory limit: {exception}\n")
