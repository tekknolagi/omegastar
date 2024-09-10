# Copyright (c) Meta Platforms, Inc. and affiliates.
# Copyright (c) Maxwell Bernstein
import logging


# Return two halves of the given list. For odd-length lists, the second half
# will be larger.
def split_list(items):
    half = len(items) // 2
    return items[0:half], items[half:]


# Attempt to reduce the `items` argument as much as possible, returning the
# shorter version. `fixed` will always be used as part of the items when
# running `command`.
# `command` should return True if the command succeeded (the failure did not
# reproduce) and False if the command failed (the failure reproduced).
def bisect_impl(command, fixed, items, indent=""):
    logging.info(f"{indent}step fixed[{len(fixed)}] and items[{len(items)}]")

    while len(items) > 1:
        logging.info(f"{indent}{len(fixed) + len(items)} candidates")

        left, right = split_list(items)
        if not command(fixed + left):
            items = left
            continue
        if not command(fixed + right):
            items = right
            continue

        # We need something from both halves to trigger the failure. Try
        # holding each half fixed and bisecting the other half to reduce the
        # candidates.
        new_right = bisect_impl(command, fixed + left, right, indent + "< ")
        new_left = bisect_impl(command, fixed + new_right, left, indent + "> ")
        return new_left + new_right

    return items


def run_bisect(command, items):
    logging.info("Verifying items")
    if command(items):
        raise ValueError("Command succeeded with full items")
    if not command([]):
        raise ValueError("Command failed with empty items")

    return bisect_impl(command, [], items)
