# Copyright (c) Meta Platforms, Inc. and affiliates.
# Copyright (c) Maxwell Bernstein
import logging


# Attempt to reduce the `items` argument as much as possible, returning the
# shorter version. `fixed` will always be used as part of the items when
# running `command`.
# `command` should return True if the command succeeded (the failure did not
# reproduce) and False if the command failed (the failure reproduced).
def bisect_impl(command, fixed, items, indent=""):
    logging.info(f"{indent}step fixed[{len(fixed)}] and items[{len(items)}]")

    while len(items) > 1:
        logging.info(f"{indent}{len(fixed) + len(items)} candidates")

        # Return two halves of the given list. For odd-length lists, the second
        # half will be larger.
        half = len(items) // 2
        left = items[0:half]
        right = items[half:]
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
    #if command(items):
    #    raise ValueError("Command succeeded with full items")
    #if not command([]):
    #    raise ValueError("Command failed with empty items")

    return bisect_impl(command, [], items)

## Optional shell integration:

import shlex
import subprocess
import sys
import textwrap


def run(
    cmd,
    verbose=True,
    cwd=None,
    check=True,
    capture_output=False,
    encoding="utf-8",
    # Specify an integer number of seconds
    timeout=-1,
    **kwargs,
):
    if verbose:
        info = "$ "
        if cwd is not None:
            info += f"cd {cwd}; "
        info += " ".join(shlex.quote(c) for c in cmd)
        if capture_output:
            info += " >& ..."
        lines = textwrap.wrap(
            info,
            break_on_hyphens=False,
            break_long_words=False,
            replace_whitespace=False,
            subsequent_indent="  ",
        )
        print(" \\\n".join(lines))
    if timeout != -1:
        cmd = ["timeout", "--signal=KILL", f"{timeout}s", *cmd]
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            capture_output=capture_output,
            encoding=encoding,
            **kwargs,
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == -9:
            # Error code from `timeout` command signaling it had to be killed
            raise TimeoutError("Command timed out", cmd)
        raise

import tempfile
import os

def write_items_to_file(items, file):
    for item in items:
        file.write(item)
    file.flush()

def run_bisect_shell(shell_command, filename):
    def command(items):
        with tempfile.NamedTemporaryFile() as f:
            write_items_to_file(items, f)
            exit_code = run([*shell_command, f.name], check=False)
        return exit_code == 0
    with open(filename, "rb") as f:
        items = f.readlines()
    return run_bisect(command, items)

if __name__ == "__main__":
    shell_command = shlex.split(sys.argv[1])
    items = run_bisect_shell(shell_command, sys.argv[2])
    fd, filename = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        write_items_to_file(items, f)
    print("Result saved in", filename)