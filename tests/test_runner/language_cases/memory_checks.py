"""Memory limit checks."""

import io
import sys

from ..cli_support import expect_equal
from .outcome import patched


class _FakeResource:
    RLIMIT_AS = 9
    RLIM_INFINITY = -1

    def __init__(self, hard_limit, fail_on_set=False):
        self.hard_limit = hard_limit
        self.fail_on_set = fail_on_set
        self.set_calls = []

    def getrlimit(self, which):
        return (self.RLIM_INFINITY, self.hard_limit)

    def setrlimit(self, which, limits):
        if self.fail_on_set:
            raise ValueError("denied")

        self.set_calls.append((which, limits))


def _capture_stderr():
    return patched(sys, stderr=io.StringIO())


def _memory_limit_uses_the_requested_size():
    from gladlang.core.util import memory

    fake = _FakeResource(hard_limit=_FakeResource.RLIM_INFINITY)
    with patched(memory, resource=fake):
        memory.set_memory_limit(100)

    expect_equal(
        fake.set_calls, [(9, (100 * 1024 * 1024, -1))], "soft limit equals the request"
    )


def _memory_limit_never_exceeds_the_hard_limit():
    from gladlang.core.util import memory

    hard = 50 * 1024 * 1024
    fake = _FakeResource(hard_limit=hard)
    with patched(memory, resource=fake):
        memory.set_memory_limit(100)

    expect_equal(
        fake.set_calls, [(9, (hard, hard))], "soft limit is capped by the hard limit"
    )


def _memory_limit_failure_is_a_warning():
    from gladlang.core.util import memory

    fake = _FakeResource(hard_limit=_FakeResource.RLIM_INFINITY, fail_on_set=True)
    with patched(memory, resource=fake), _capture_stderr():
        memory.set_memory_limit(100)
        text = sys.stderr.getvalue()

    expect_equal(text, "Warning: Could not set memory limit: denied\n", "warning text")


def _memory_limit_is_skipped_without_the_resource_module():
    from gladlang.core.util import memory

    with patched(memory, resource=None), _capture_stderr():
        memory.set_memory_limit(64)
        text = sys.stderr.getvalue()

    expect_equal(text, "", "no warning and no crash when resource is unavailable")
