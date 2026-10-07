"""Regression tests for the PARI owner runtime's process lifecycle."""

import os
import signal
import subprocess
import sys
import tempfile
import unittest


class TestRuntimeRegressions(unittest.TestCase):
    @unittest.skipUnless(hasattr(os, "fork"), "requires os.fork")
    def test_fork_restriction_survives_another_fork(self):
        code = r'''
import os
import traceback
import warnings

from cypari2 import Pari

pari = Pari()
value = pari(41)

def assert_rejected():
    for operation in (lambda: pari(1), lambda: value + 1):
        try:
            operation()
        except RuntimeError as exc:
            assert "spawn" in str(exc), str(exc)
        else:
            raise AssertionError("forked process accepted inherited PARI state")

def fork_and_wait(operation):
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message=r"This process .* is multi-threaded",
            category=DeprecationWarning)
        child = os.fork()
    if child == 0:
        try:
            operation()
        except BaseException:
            traceback.print_exc()
            os._exit(1)
        os._exit(0)
    _, status = os.waitpid(child, 0)
    assert os.waitstatus_to_exitcode(status) == 0, status

def first_child():
    assert_rejected()
    fork_and_wait(assert_rejected)

fork_and_wait(first_child)
assert pari(1) == 1
assert value + 1 == 42
'''
        with tempfile.TemporaryDirectory() as directory:
            with subprocess.Popen(
                    [sys.executable, "-c", code],
                    cwd=directory,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True) as process:
                try:
                    stdout, stderr = process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    # Stop descendants too if a regression deadlocks either
                    # fork. Normally both children are reaped by waitpid.
                    os.killpg(process.pid, signal.SIGKILL)
                    stdout, stderr = process.communicate()
                    self.fail(f"fork regression timed out:\n{stdout}{stderr}")
        self.assertEqual(process.returncode, 0, stdout + stderr)


if __name__ == "__main__":
    unittest.main()
