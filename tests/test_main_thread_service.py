"""Exercise the main-thread PARI service and its downstream Cython boundary."""

from concurrent.futures import ThreadPoolExecutor
from contextvars import ContextVar
from inspect import signature
import os
import signal
import subprocess
import sys
from threading import get_ident
import unittest

from cypari2 import Gen, Pari, PariError
from cypari2.closure import objtoclosure
from cypari2.test import call_with_sig_on, caller_has_pari_stack


class MainThreadServiceTests(unittest.TestCase):
    def setUp(self):
        self.pari = Pari()

    def test_pool_and_shared_values(self):
        pari = self.pari
        main = get_ident()
        before = pari(41)

        def application():
            with ThreadPoolExecutor(max_workers=4) as pool:
                self.assertEqual(pool.submit(pari.issquarefree, 15).result(), 1)
                self.assertEqual(pool.submit(pari.run_on_owner, get_ident).result(), main)
                self.assertTrue(pool.submit(pari.run_on_owner, caller_has_pari_stack).result())
                values = list(pool.map(lambda i: before + i, range(64)))
                vector = pool.submit(pari, values).result()
                self.assertEqual(list(vector), values)
                return vector

        self.assertTrue(caller_has_pari_stack())
        vector = pari.run_with_threads(application)
        self.assertEqual(vector[63], 104)
        self.assertTrue(caller_has_pari_stack())

    def test_first_call_via_module_helper(self):
        for expression in ("integer_to_gen(15)", "objtogen(15)", "objtoclosure(lambda: 15)()"):
            subprocess.run([sys.executable, "-P", "-c",
                            "from cypari2.closure import objtoclosure\n"
                            "from cypari2.convert import integer_to_gen\n"
                            "from cypari2.gen import objtogen\n"
                            f"assert {expression} == 15"], check=True, timeout=15)

    def test_no_service(self):
        with ThreadPoolExecutor(max_workers=1) as pool:
            for function, args in ((Pari, ()), (self.pari.issquarefree, (15,)),
                                   (objtoclosure, (lambda: 1,)),
                                   (int, (self.pari(99),))):
                with self.assertRaisesRegex(RuntimeError, "main thread"):
                    pool.submit(function, *args).result()

    def test_typed_keyword_converted_on_owner(self):
        calls = []
        main = get_ident()

        class IntegerArgument:
            def __int__(self):
                calls.append(get_ident())
                return 8

            __index__ = __int__

        fibonacci = self.pari.fibonacci
        self.assertEqual(tuple(signature(fibonacci).parameters), ("x",))
        index = IntegerArgument()
        with ThreadPoolExecutor(max_workers=1) as pool:
            with self.assertRaisesRegex(RuntimeError, "main thread"):
                pool.submit(fibonacci, x=index).result()
        self.assertEqual(calls, [])

        self.assertEqual(self.pari.run_with_threads(fibonacci, x=index), 21)
        self.assertEqual(calls, [main])

    def test_callback_context_and_error_recovery(self):
        pari = self.pari
        var = ContextVar("value", default=0)
        main = get_ident()

        def callback():
            self.assertEqual(get_ident(), main)
            return pari(var.get()) + 1

        f = pari(callback)

        def application():
            var.set(14)
            self.assertEqual(objtoclosure(callback)(), 15)
            self.assertEqual(f(), 15)
            with self.assertRaises(PariError) as caught:
                pari(1) / 0
            self.assertIsInstance(caught.exception.errdata(), Gen)
            self.assertEqual(f(), 15)

        pari.run_with_threads(application)
        self.assertEqual(f(), 1)
        self.assertEqual(var.get(), 0)

    def test_foreign_signal_frame_and_reentry(self):
        pari = self.pari

        def application():
            with self.assertRaisesRegex(RuntimeError, "signal frame"):
                call_with_sig_on(lambda: pari(7))
            with self.assertRaisesRegex(RuntimeError, "idle main thread"):
                pari.run_on_owner(pari.run_with_threads, lambda: None)
            return pari(5)

        self.assertEqual(pari.run_with_threads(application), 5)

    def test_worker_drops_last_clone_after_service(self):
        # Indexing creates a shared clone. The child reference survives both
        # the producing thread and the vector, then dies on a different thread.
        for _ in range(10):
            items = [self.pari.run_with_threads(lambda: self.pari("[[1,2],3]")[0])]
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(items.clear).result()
            self.assertEqual(self.pari("[4,5]")[1], 5)

    @unittest.skipUnless(hasattr(signal, "SIGALRM"), "requires SIGALRM")
    def test_interrupt_during_worker_request(self):
        subprocess.run([sys.executable, "-P", "-c", """
from cypari2 import Pari
from cysignals.alarm import AlarmInterrupt, alarm, cancel_alarm
p = Pari()

def interruptible():
    alarm(0.05)
    try:
        p("while(1,)")
    finally:
        cancel_alarm()

def application():
    try:
        p.run_on_owner(interruptible)
    except AlarmInterrupt:
        return p(17)
    raise AssertionError("request did not observe the alarm")

assert p.run_with_threads(application) == 17
assert p(5) + 1 == 6
"""], timeout=20, check=True)

    def test_application_exception_stops_service(self):
        def fail():
            raise ValueError("application failed")

        with self.assertRaisesRegex(ValueError, "application failed"):
            self.pari.run_with_threads(fail)
        self.assertEqual(self.pari.run_with_threads(self.pari, 123), 123)

    @unittest.skipUnless(hasattr(os, "fork"), "requires os.fork")
    def test_fork_after_pari_initialization(self):
        subprocess.run([sys.executable, "-P", "-c", """
import os
from cypari2 import Pari
p = Pari()
x = p(41)
assert p.run_with_threads(lambda: x + 1) == 42
pid = os.fork()
if not pid:
    os._exit(0 if x + 1 == 42 else 1)
assert os.waitpid(pid, 0)[1] == 0
assert x + 1 == 42
"""], timeout=20, check=True)
