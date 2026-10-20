"""Runs a list of named checks and counts the results."""

import sys

from .assertions import Skip


def run_checks(group, checks, passed_count, failed_count, failure_list):
    for entry in checks:
        name, check = entry[0], entry[1]
        known_issue = entry[2] if len(entry) > 2 else None
        label = f"{group}::{name}"

        sys.stdout.write(f"\n\nRunning {label}... \n")
        sys.stdout.flush()

        try:
            check()
        except Skip as reason:
            passed_count += 1
            sys.stdout.write(f"SKIP ({reason})\n")
            continue
        except AssertionError as problem:
            if known_issue:
                passed_count += 1
                sys.stdout.write(f"XFAIL (known issue: {known_issue})\n")
            else:
                failed_count += 1
                failure_list.append((label, str(problem) or "assertion failed"))
                sys.stdout.write("FAIL\n")
            continue
        except Exception as exception:
            failed_count += 1
            failure_list.append((label, f"{type(exception).__name__}: {exception}"))
            sys.stdout.write("CRASH\n")
            continue

        if known_issue:
            failed_count += 1
            failure_list.append(
                (
                    label,
                    f"Known issue appears fixed ({known_issue}). "
                    "Remove the known-issue marker so this becomes a normal test.",
                )
            )
            sys.stdout.write("FAIL (unexpected pass)\n")
        else:
            passed_count += 1
            sys.stdout.write("PASS\n")

    return passed_count, failed_count, failure_list
