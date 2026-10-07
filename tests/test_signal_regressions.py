"""Regression coverage for Cython clients of the Python owner-thread API."""

import os
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from cypari2 import Pari, PariError
from cypari2.test import (call_with_sig_on, cython_power,
                         gen_from_complex, gen_from_double)


class SignalContextTests(unittest.TestCase):
    def run_in_fresh_process(self, code):
        # Run crash regressions outside the test runner, and outside the
        # source directory so they import the installed extension modules.
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=directory,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=10,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_foreign_signal_frame_before_initialization(self):
        self.run_in_fresh_process('''
from cypari2 import Pari
from cypari2.test import call_with_sig_on
try:
    call_with_sig_on(Pari)
except RuntimeError as exc:
    assert "sig_on() block" in str(exc), str(exc)
else:
    raise AssertionError("initialization accepted a foreign signal frame")
assert Pari()(2) == 2
''')

    def test_foreign_signal_frame_after_initialization(self):
        self.run_in_fresh_process('''
from cypari2 import Pari
from cypari2.test import call_with_sig_on
p = Pari()
called = []
def evaluate():
    called.append(True)
    return p("1/0")
try:
    call_with_sig_on(evaluate)
except RuntimeError as exc:
    assert "sig_on() block" in str(exc), str(exc)
else:
    raise AssertionError("evaluation accepted a foreign signal frame")
assert called == [True]
assert p(3) == 3
''')

    def test_conversion_helpers_initialize_owner(self):
        for expression, expected in (
                ("gen_from_double(1.25)", "1.25"),
                ("gen_from_complex(1.25, -2.5)", "1.25 - 2.5j")):
            with self.subTest(expression=expression):
                self.run_in_fresh_process(f'''
from cypari2.test import gen_from_double, gen_from_complex
value = {expression}
assert complex(value) == {expected}
''')

    def test_conversion_helpers_work_on_python_workers(self):
        p = Pari()
        with ThreadPoolExecutor(max_workers=2) as executor:
            real = executor.submit(gen_from_double, 1.25).result(timeout=5)
            value = executor.submit(gen_from_complex, 1.25, -2.5).result(timeout=5)
        self.assertEqual(real, p("5/4"))
        self.assertEqual(value, p("5/4 - 5/2*I"))

    def test_raw_cython_computation_runs_on_owner(self):
        p = Pari()
        value = p.run_on_owner(cython_power, 3, exponent=4)
        self.assertEqual(value, 81)
        self.assertEqual(value + 1, 82)
        with self.assertRaises(PariError):
            p.run_on_owner(cython_power, 0, exponent=-1)
        self.assertEqual(p(3), 3)

    def test_request_queues_while_owner_has_a_signal_frame(self):
        p = Pari()
        entered = threading.Event()
        release = threading.Event()

        def wait_on_owner():
            entered.set()
            if not release.wait(5):
                raise AssertionError("test did not release the owner")

        with ThreadPoolExecutor(max_workers=2) as executor:
            active = executor.submit(
                p.run_on_owner, call_with_sig_on, wait_on_owner)
            try:
                self.assertTrue(entered.wait(5))
                queued = executor.submit(p, 17)
                with self.assertRaises(TimeoutError):
                    queued.result(timeout=0.1)
            finally:
                release.set()
            active.result(timeout=5)
            self.assertEqual(queued.result(timeout=5), 17)


if __name__ == "__main__":
    unittest.main()
