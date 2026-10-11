"""Runs the Class copy cache-isolation check."""

import sys

from .helpers import check_class_copy_cache_isolation


def run_class_copy_check(passed_count, failed_count, failure_list):
    try:
        check_class_copy_cache_isolation()
        passed_count += 1
        sys.stdout.write("PASS: class copy cache isolation\n")
    except Exception as exception:
        failed_count += 1
        failure_list.append(("class_copy_cache_isolation", str(exception)))
        sys.stdout.write("FAIL: class copy cache isolation\n")

    return passed_count, failed_count, failure_list
