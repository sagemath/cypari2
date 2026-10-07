"""Helpers for tests that need a fresh interpreter and installed extensions."""

import subprocess
import sys
import tempfile


def run_in_fresh_process(code, *, python_args=(), timeout=10):
    """Run code outside the source directory and return its captured stdout."""
    with tempfile.TemporaryDirectory() as directory:
        completed = subprocess.run(
            [sys.executable, *python_args, "-c", code],
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    if completed.returncode:
        raise AssertionError(
            f"Python subprocess exited with {completed.returncode}:\n"
            f"{completed.stdout}{completed.stderr}")
    return completed.stdout
