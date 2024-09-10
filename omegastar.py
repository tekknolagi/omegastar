#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.

import logging


# Return two halves of the given list. For odd-length lists, the second half
# will be larger.
def split_list(items):
    half = len(items) // 2
    return items[0:half], items[half:]


# Attempt to reduce the `jitlist` argument as much as possible, returning the
# shorter version. `fixed` will always be used as part of the jitlist when
# running `command`.
# `command` should return True if the command succeeded (the failure did not
# reproduce) and False if the command failed (the failure reproduced).
def bisect_impl(command, fixed, jitlist, indent=""):
    logging.info(f"{indent}step fixed[{len(fixed)}] and jitlist[{len(jitlist)}]")

    while len(jitlist) > 1:
        logging.info(f"{indent}{len(fixed) + len(jitlist)} candidates")

        left, right = split_list(jitlist)
        if not command(fixed + left):
            jitlist = left
            continue
        if not command(fixed + right):
            jitlist = right
            continue

        # We need something from both halves to trigger the failure. Try
        # holding each half fixed and bisecting the other half to reduce the
        # candidates.
        new_right = bisect_impl(command, fixed + left, right, indent + "< ")
        new_left = bisect_impl(command, fixed + new_right, left, indent + "> ")
        return new_left + new_right

    return jitlist


def run_bisect(command, jitlist):
    logging.info("Verifying jit-list")
    if command(jitlist):
        raise ValueError("Command succeeded with full jit-list")
    if not command([]):
        raise ValueError("Command failed with empty jit-list")

    return bisect_impl(command, [], jitlist)
