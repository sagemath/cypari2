"""Regression tests for stack values retained by reentrant callbacks."""

import unittest

from cypari2 import Pari, PariError


class TestCallbackStackLifetime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pari = Pari()

    def test_nested_callback_indexes_outer_stack_value(self):
        def outer():
            value = self.pari.vector(2)
            return self.pari(lambda: value[0])()

        self.assertEqual(self.pari(outer)(), 0)

    def test_python_exception_leaves_evaluator_usable(self):
        failure = ValueError("callback failed")

        def fail():
            raise failure

        callback = self.pari(fail)
        invoke = self.pari("f -> iferr(f(), E, 99)")
        with self.assertRaises(ValueError) as caught:
            invoke(callback)
        self.assertIs(caught.exception, failure)
        # A callback returning normally must reinstate GP's error handler.
        recover = self.pari("f -> iferr(f(); 1/0, E, 99)")
        self.assertEqual(recover(self.pari(lambda: 7)), 99)
        with self.assertRaises(PariError):
            self.pari(1) / self.pari(0)

    def test_outer_callback_can_handle_inner_python_exception(self):
        def fail():
            raise ValueError("inner callback failed")

        inner = self.pari(fail)

        def outer():
            symbol = self.pari("callback_variable")
            with self.assertRaisesRegex(ValueError, "inner callback failed"):
                inner()
            self.assertEqual(str(symbol), "callback_variable")
            return self.pari(40) + 2

        invoke = self.pari("f -> 1 + f()")
        self.assertEqual(invoke(self.pari(outer)), 43)
        with self.assertRaises(PariError):
            self.pari(1) / self.pari(0)

    def test_callback_cannot_replace_active_stack(self):
        size = self.pari.stacksize()
        with self.assertRaisesRegex(RuntimeError, "during a Python callback"):
            self.pari(lambda: self.pari.allocatemem(2 * size, silent=True))()
        self.assertEqual(self.pari.stacksize(), size)
        self.assertEqual(self.pari(6) * 7, 42)

    def test_callback_result_exceeds_half_stack(self):
        size = self.pari.stacksize()
        sizemax = self.pari.stacksizemax()
        try:
            self.pari.allocatemem(8_000_000, silent=True)
            result = self.pari(lambda: self.pari.vector(600_000))()
            self.assertEqual(len(result), 600_000)
            self.assertEqual(result[0], 0)
            self.assertEqual(result[599_999], 0)
        finally:
            self.pari.allocatemem(size, sizemax, silent=True)

    def check_retained_value_after_guard_move(self, fail):
        saved = []

        def outer():
            value = self.pari.vector(2)

            def inner():
                # Indexing an older stack vector moves it and the callback
                # guards to the heap.  Create a new stack value afterwards.
                value[0]
                saved.append(self.pari(123456789))
                if fail:
                    raise ValueError("callback failed after indexing")
                return 17

            return self.pari(inner)()

        if fail:
            with self.assertRaisesRegex(ValueError, "callback failed after indexing"):
                self.pari(outer)()
        else:
            self.assertEqual(self.pari(outer)(), 17)

        # Reuse PARI's stack before examining the retained callback value.
        self.pari.vector(1000)
        self.assertEqual(saved[0] + 1, 123456790)

    def test_callback_retains_value_after_guard_move(self):
        self.check_retained_value_after_guard_move(False)

    def test_callback_exception_retains_value_after_guard_move(self):
        self.check_retained_value_after_guard_move(True)


if __name__ == "__main__":
    unittest.main()
