#!/usr/bin/env python

import contextvars
import gc
import os
import signal
import subprocess
import sys
import tempfile
import threading
import unittest
import warnings
import weakref
from concurrent.futures import ThreadPoolExecutor

import cypari2
from cypari2.convert import gen_to_python, integer_to_gen
from cypari2.test import pari_mt_engine


class TestThreadSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pari = cypari2.Pari()

    def require_pari_pthread_workers(self):
        engine = pari_mt_engine()
        if engine != "pthread":
            self.skipTest(f"requires PARI pthread engine, found {engine!r}")

    def test_original_issue_without_executor_initializer(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.pari.issquarefree, 15)
            self.assertEqual(future.result(timeout=10), 1)

    def test_gen_survives_creating_thread(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            value = executor.submit(self.pari, "[1, 2, 3]").result(timeout=10)

        self.assertEqual(repr(value), "[1, 2, 3]")
        self.assertEqual([int(entry) for entry in value], [1, 2, 3])
        value[1] = 9
        self.assertEqual(repr(value), "[1, 9, 3]")

    def test_same_gen_from_many_threads(self):
        value = self.pari("[1, 2, 3, 4]")

        def inspect_value(index):
            return int(value[index]), repr(value + value)

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(inspect_value, i % 4) for i in range(200)]
            results = [future.result(timeout=10) for future in futures]

        self.assertEqual(results[0], (1, "[2, 4, 6, 8]"))
        self.assertEqual(results[-1], (4, "[2, 4, 6, 8]"))

    def test_same_gen_can_be_mutated_from_many_threads(self):
        value = self.pari.vector(100)

        def set_entry(index):
            value[index] = index + 1

        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(set_entry, range(100)))
        self.assertEqual([int(entry) for entry in value], list(range(1, 101)))

    def test_gen_iterator_is_lazy_and_thread_safe(self):
        value = self.pari([1, 2, 3])
        iterator = iter(value)
        value[0] = 9
        self.assertEqual(next(iterator), 9)
        self.assertEqual([int(entry) for entry in iterator], [2, 3])
        self.assertIsNot(next(iter(value)), next(iter(value)))
        with self.assertRaises(StopIteration):
            next(iterator)
        with self.assertRaises(TypeError):
            iter(self.pari(42))

        iterator = iter(self.pari(range(40)))
        with ThreadPoolExecutor(max_workers=8) as executor:
            entries = list(executor.map(lambda _: next(iterator), range(40)))
        self.assertEqual(sorted(map(int, entries)), list(range(40)))
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_owner_callback_iterator_can_escape_safely(self):
        saved = []

        def save_iterator():
            # Polynomial iteration creates a temporary coefficient vector on
            # the PARI stack; the proxy must survive stabilization of it.
            saved.append(iter(self.pari("1 + 2*x + 3*x^2")))
            return 0

        self.assertEqual(self.pari(save_iterator)(), 0)
        with ThreadPoolExecutor(max_workers=1) as executor:
            entries = executor.submit(list, saved.pop()).result(timeout=10)
        self.assertEqual(list(map(int, entries)), [1, 2, 3])

    def test_pari_subclass_helpers_stay_on_calling_thread(self):
        class PariSubclass(cypari2.Pari):
            def current_thread(self):
                return threading.get_ident()

        pari = PariSubclass()
        self.assertEqual(pari.current_thread(), threading.get_ident())

        def identify_thread():
            return threading.get_ident(), pari.current_thread()

        with ThreadPoolExecutor(max_workers=1) as executor:
            caller, observed = executor.submit(identify_thread).result(timeout=10)
        self.assertEqual(observed, caller)
        self.assertEqual(pari.issquarefree(15), 1)

    def test_results_can_be_destroyed_on_worker_threads(self):
        def create_and_destroy(n):
            value = self.pari(n).nextprime()
            text = repr(value)
            del value
            gc.collect()
            return text

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(create_and_destroy, range(1, 201)))

        self.assertEqual(results[0], "2")
        self.assertTrue(results[-1])
        # Submit one more operation so all previously queued clone releases
        # have run on the PARI owner thread.
        self.assertEqual(self.pari(1), 1)

    def test_clone_release_can_reenter_enqueue_lock(self):
        code = r'''
import gc

from cypari2 import Pari
from cypari2._thread_runtime import runtime

pari = Pari()
value = pari(123)
# Ensure that owner-side bookkeeping for the result has completed.
pari(0)
with runtime._queue_lock:
    del value
    gc.collect()
print(pari(42))
'''
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=directory,
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "42")

    def test_clone_heap_is_reclaimed_after_worker_use(self):
        from cypari2._thread_runtime import runtime

        def drain_releases():
            gc.collect()
            runtime.call(lambda: None)
            gc.collect()
            runtime.call(lambda: None)

        def heap_usage():
            usage = tuple(self.pari.getheap().python())
            drain_releases()
            return usage

        def create_and_destroy(n):
            return int(self.pari(n).nextprime() + 1)

        drain_releases()
        baseline = heap_usage()
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(create_and_destroy, range(1, 1001)))
        self.assertEqual(heap_usage(), baseline)

    def test_exceptions_cross_thread_boundary(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.pari, "1/0")
            with self.assertRaises(cypari2.PariError):
                future.result(timeout=10)

    def test_context_variables_cross_thread_boundary(self):
        from cypari2._thread_runtime import runtime

        marker = contextvars.ContextVar("cypari2_test_marker")

        def read_and_mutate():
            value = marker.get()
            marker.set(f"owner:{value}")
            return value

        def call_from_context(value):
            token = marker.set(value)
            try:
                return runtime.call(read_and_mutate), marker.get()
            finally:
                marker.reset(token)

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(
                call_from_context, (f"caller:{i}" for i in range(64))))

        self.assertEqual(
            results,
            [(f"caller:{i}", f"caller:{i}") for i in range(64)],
        )
        self.assertEqual(
            runtime.call(lambda: marker.get("unset")), "unset")

        class Payload:
            pass

        payload = Payload()
        payload_ref = weakref.ref(payload)
        token = marker.set(payload)
        try:
            runtime.call(lambda: None)
        finally:
            marker.reset(token)
        del payload
        gc.collect()
        self.assertIsNone(payload_ref())

    def test_call_completes_after_request_context_exits(self):
        from cypari2._thread_runtime import _PariThreadRuntime

        request_finished = threading.Event()
        release_context = threading.Event()

        class PausingRuntime(_PariThreadRuntime):
            def _run_request(inner_self, request):
                super()._run_request(request)
                request_finished.set()
                release_context.wait()

        runtime = PausingRuntime()
        runtime.install_initializer(lambda: None)
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(runtime.call, lambda: 42)
                self.assertTrue(request_finished.wait(timeout=10))
                try:
                    self.assertFalse(future.done())
                finally:
                    release_context.set()
                self.assertEqual(future.result(timeout=10), 42)
        finally:
            release_context.set()
            runtime.shutdown()

    @unittest.skipIf(
        sys.version_info < (3, 14),
        "context-aware warnings require Python 3.14",
    )
    def test_context_aware_warnings_cross_thread_boundary(self):
        code = r'''
import sys
import warnings

from cypari2 import Pari

assert sys.flags.context_aware_warnings
pari = Pari()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    pari("[2,1;2,1]").matkerint(1)
assert len(caught) == 1, caught
assert issubclass(caught[0].category, DeprecationWarning)
'''
        completed = subprocess.run(
            [sys.executable, "-X", "context_aware_warnings=1", "-c", code],
            cwd=os.getcwd(),
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    @unittest.skipIf(
        sys.version_info < (3, 14),
        "explicit thread contexts require Python 3.14",
    )
    def test_owner_thread_does_not_retain_creator_context(self):
        code = r'''
import contextvars
import gc
import sys
import weakref

from cypari2._thread_runtime import _PariThreadRuntime

assert sys.flags.thread_inherit_context
runtime = _PariThreadRuntime()
runtime.install_initializer(lambda: None)

class Payload:
    pass

marker = contextvars.ContextVar("cypari2_test_creator_marker")
payload = Payload()
payload_ref = weakref.ref(payload)
token = marker.set(payload)
runtime.call(lambda: None)
marker.reset(token)
del payload

# Advance the owner loop so neither its local request nor its per-request
# context can retain the payload.  Its Thread bootstrap context must not do so.
runtime.call(lambda: None)
for _ in range(3):
    gc.collect()
assert payload_ref() is None, payload_ref()
runtime.shutdown()
'''
        completed = subprocess.run(
            [sys.executable, "-X", "thread_inherit_context=1", "-c", code],
            cwd=os.getcwd(),
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_python_callback_is_reentrant_on_owner(self):
        closure = self.pari(lambda value: value + 1)
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(closure, 41).result(timeout=10)
        self.assertEqual(result, 42)

    def test_method_captured_on_owner_remains_safe(self):
        captured = []
        value = self.pari(17)

        def capture_methods():
            captured.extend([self.pari.issquarefree, value.nextprime])

        self.pari(capture_methods)()
        with ThreadPoolExecutor(max_workers=2) as executor:
            squarefree = executor.submit(captured[0], 15).result(timeout=10)
            next_prime = executor.submit(captured[1]).result(timeout=10)
        self.assertEqual(squarefree, 1)
        self.assertEqual(next_prime, 17)

    def test_unbound_extension_methods_dispatch_to_owner(self):
        value = self.pari(16)
        with ThreadPoolExecutor(max_workers=3) as executor:
            squarefree = executor.submit(
                type(self.pari).issquarefree, self.pari, 15)
            square_root = executor.submit(type(value).sqrt, value)
            next_prime = executor.submit(type(value).nextprime, value)
            self.assertEqual(squarefree.result(timeout=10), 1)
            self.assertEqual(square_root.result(timeout=10), 4)
            self.assertEqual(next_prime.result(timeout=10), 17)

    def test_nested_pari_error_in_python_callback_is_safe(self):
        multiply = self.pari(lambda left, right: left * right)
        with self.assertRaises(cypari2.PariError):
            multiply([1], [2])

        # The nested error must not longjmp across the callback's Python
        # frames and corrupt the owner thread.
        self.assertEqual(self.pari(41) + 1, 42)

        def catch_nested_error():
            try:
                self.pari("1/0")
            except cypari2.PariError:
                return self.pari(42)

        with self.assertRaisesRegex(RuntimeError, "cannot be caught"):
            self.pari(catch_nested_error)()
        self.assertEqual(self.pari(42), 42)

        class CallbackResult:
            def __str__(inner_self):
                try:
                    self.pari("1/0")
                except cypari2.PariError:
                    return "42"

        with self.assertRaisesRegex(RuntimeError, "cannot be caught"):
            self.pari(lambda: CallbackResult())()
        self.assertEqual(self.pari(42), 42)

        # PARI's own iferr recovery is contained inside the nested call and
        # must not be confused with a PariError suppressed by Python.
        self.assertEqual(
            self.pari(lambda: self.pari("iferr(1/0, E, 42)"))(),
            42,
        )

    def test_python_callback_side_effect_gen_is_stabilized(self):
        saved = []

        def save_value():
            saved.append(self.pari(123456789))
            return 0

        self.assertEqual(self.pari(save_value)(), 0)
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(lambda: saved.pop() + 1).result(timeout=10)
        self.assertEqual(result, 123456790)

    def test_python_callback_exception_stabilizes_side_effect_gen(self):
        saved = []

        def save_then_raise():
            saved.append(self.pari(41))
            raise ValueError("callback failed")

        with self.assertRaisesRegex(ValueError, "callback failed"):
            self.pari(save_then_raise)()
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(lambda: saved.pop() + 1).result(timeout=10)
        self.assertEqual(result, 42)

    def test_stack_gen_can_be_destroyed_on_worker_during_callback(self):
        saved = []

        with ThreadPoolExecutor(max_workers=1) as executor:
            def create_and_release_elsewhere():
                saved.extend(self.pari(123456789 + i) for i in range(64))

                def release():
                    saved.clear()
                    gc.collect()

                executor.submit(release).result(timeout=10)
                return 0

            self.assertEqual(self.pari(create_and_release_elsewhere)(), 0)

        self.assertEqual(self.pari(41) + 1, 42)

    def test_python_conversion_side_effect_gen_is_stabilized(self):
        saved = []
        old_level = self.pari.get_debug_level()

        class DebugLevel:
            def __int__(inner_self):
                saved.append(self.pari(72))
                return old_level

        self.pari.set_debug_level(DebugLevel())
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(lambda: saved.pop() + 1).result(timeout=10)
        self.assertEqual(result, 73)

        class FailingDebugLevel:
            def __int__(inner_self):
                saved.append(self.pari(99))
                raise ValueError("conversion failed")

        with self.assertRaisesRegex(ValueError, "conversion failed"):
            self.pari.set_debug_level(FailingDebugLevel())
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(lambda: saved.pop() + 1).result(timeout=10)
        self.assertEqual(result, 100)

    def test_python_callback_in_pari_worker_fails_safely(self):
        self.require_pari_pthread_workers()
        old_threads = int(self.pari.default("nbthreads"))
        try:
            self.pari.default("nbthreads", 2)

            with self.assertRaisesRegex(
                    cypari2.PariError, "set nbthreads to 1"):
                self.pari.parapply(lambda value: value + 1, range(4))

            # Native PARI closures retain PARI's internal parallelism.
            native = self.pari("value -> value + 1")
            self.assertEqual(
                list(self.pari.parapply(native, range(4))),
                [1, 2, 3, 4],
            )

            self.pari.default("nbthreads", 1)
            self.assertEqual(
                list(self.pari.parapply(lambda value: value + 1, range(4))),
                [1, 2, 3, 4],
            )
        finally:
            self.pari.default("nbthreads", old_threads)

    def test_stack_resize_callback_in_pari_worker_fails_safely(self):
        self.require_pari_pthread_workers()
        old_threads = int(self.pari.default("nbthreads"))
        try:
            self.pari.default("nbthreads", 2)

            for setting in ("parisize", "parisizemax"):
                expression = (
                    f"parapply(x -> default({setting}), [1, 2, 3, 4])"
                )
                with self.assertRaisesRegex(
                        cypari2.PariError, "cannot run in a PARI worker"):
                    self.pari(expression)
                self.assertEqual(self.pari(42), 42)
        finally:
            self.pari.default("nbthreads", old_threads)

    def test_pari_worker_output_does_not_enter_python(self):
        self.require_pari_pthread_workers()
        code = r'''
from cypari2 import Pari
pari = Pari()
pari.default("nbthreads", 2)
pari("parapply(value -> print(value), [1, 2, 3, 4])")
print("owner still usable", pari(1))
'''
        environment = os.environ.copy()
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=directory,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("owner still usable 1", completed.stdout)

    @unittest.skipUnless(hasattr(signal, "SIGALRM"), "requires SIGALRM")
    def test_alarm_is_routed_to_owner(self):
        from cysignals.alarm import AlarmInterrupt, alarm, cancel_alarm

        try:
            alarm(0.05)
            with self.assertRaises(AlarmInterrupt):
                self.pari("while(1,)")
            with ThreadPoolExecutor(max_workers=1) as executor:
                alarm(0.05)
                future = executor.submit(self.pari, "while(1,)")
                with self.assertRaises(AlarmInterrupt):
                    future.result(timeout=10)

            # A re-entrant PARI call made by a Python callback has its own
            # cysignals frame and must not inherit the outer callback's
            # interrupt block indefinitely.
            alarm(0.05)
            with self.assertRaises(AlarmInterrupt):
                self.pari(lambda: self.pari("while(1,)"))()
        finally:
            cancel_alarm()
        self.assertEqual(self.pari(1), 1)

    def test_public_conversion_helpers(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            value = executor.submit(integer_to_gen, 2**100).result(timeout=10)
            converted = executor.submit(gen_to_python, value).result(timeout=10)
        self.assertEqual(converted, 2**100)

    def test_module_helpers_initialize_owner(self):
        code = r'''
from cypari2.closure import objtoclosure
from cypari2.convert import integer_to_gen
from cypari2.gen import objtogen
print(integer_to_gen(5), objtogen(6), objtoclosure(lambda: 7)())
'''
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, "-c", code],
                cwd=directory,
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "5 6 7")

    @unittest.skipUnless(hasattr(os, "fork"), "requires os.fork")
    def test_fork_after_initialization_fails_safely(self):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r"This process .* is multi-threaded",
                category=DeprecationWarning,
            )
            child = os.fork()
        if child == 0:
            try:
                try:
                    self.pari(1)
                except RuntimeError as exc:
                    os._exit(0 if "spawn" in str(exc) else 2)
                os._exit(3)
            except BaseException:
                os._exit(4)

        _, status = os.waitpid(child, 0)
        self.assertTrue(os.WIFEXITED(status))
        self.assertEqual(os.WEXITSTATUS(status), 0)
        self.assertEqual(self.pari(1), 1)

    def test_concurrent_pari_construction(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(cypari2.Pari) for _ in range(32)]
            instances = [future.result(timeout=10) for future in futures]
        self.assertTrue(all(instance.issquarefree(15) == 1 for instance in instances))
        self.assertTrue(all(instance.PARI_ZERO == 0 for instance in instances))


if __name__ == "__main__":
    unittest.main()
