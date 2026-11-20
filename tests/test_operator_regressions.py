"""Keep Python's operator negotiation on the calling thread."""

import operator
import threading
import unittest

from cypari2 import Gen, Pari


class TestOperatorDispatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pari = Pari()

    def test_unbound_slots_return_not_implemented(self):
        value = self.pari(3)
        for name in ("add", "sub", "mul", "truediv", "floordiv", "mod", "pow"):
            for prefix in ("__", "__r"):
                with self.subTest(method=prefix + name):
                    method = getattr(Gen, prefix + name + "__")
                    self.assertIs(method(value, object()), NotImplemented)
        for name in ("lt", "le", "eq", "ne", "gt", "ge"):
            with self.subTest(method=name):
                self.assertIs(getattr(Gen, "__" + name + "__")(value, object()),
                              NotImplemented)

    def test_left_operand_is_not_tried_again(self):
        caller = threading.get_ident()
        for name in ("add", "sub", "mul", "truediv", "floordiv", "mod", "pow",
                     "lshift", "rshift"):
            calls = []

            def first_attempt(self, other):
                calls.append(threading.get_ident())
                # Repeating negotiation must not change the result.
                return NotImplemented if len(calls) == 1 else 999

            left_type = type("Left", (), {
                "__" + name + "__": first_attempt,
                "__str__": lambda self: "6",
            })
            with self.subTest(operation=name):
                operation = getattr(operator, name)
                self.assertEqual(operation(left_type(), self.pari(2)),
                                 operation(self.pari(6), self.pari(2)))
                self.assertEqual(calls, [caller])

    def test_reflected_fallback_stays_on_caller(self):
        caller = threading.get_ident()
        for name in ("add", "sub", "mul", "truediv", "floordiv", "mod", "pow"):
            calls = []
            result = object()

            def fallback(self, other):
                calls.append(threading.get_ident())
                return result

            right_type = type("Right", (), {"__r" + name + "__": fallback})
            with self.subTest(operation=name):
                self.assertIs(getattr(operator, name)(self.pari(2), right_type()),
                              result)
                self.assertEqual(calls, [caller])

    def test_comparison_fallback_stays_on_caller(self):
        caller = threading.get_ident()
        pairs = (("lt", "gt"), ("le", "ge"), ("eq", "eq"),
                 ("ne", "ne"), ("gt", "lt"), ("ge", "le"))
        for operation, reflected in pairs:
            calls = []
            result = object()

            def fallback(self, other):
                calls.append(threading.get_ident())
                return result

            right_type = type("Right", (), {"__" + reflected + "__": fallback})
            with self.subTest(operation=operation):
                self.assertIs(getattr(operator, operation)(self.pari(2), right_type()),
                              result)
                self.assertEqual(calls, [caller])

    def test_reflected_and_modular_operations(self):
        self.assertEqual(Gen.__div__(6, self.pari(2)), 3)
        self.assertIs(Gen.__div__(self.pari(2), object()), NotImplemented)
        self.assertEqual(33 << self.pari(2), 132)
        self.assertEqual(33 >> self.pari(2), 8)
        self.assertEqual(2 ** self.pari(3), 8)
        self.assertEqual(pow(self.pari(5), 28, 29), self.pari("Mod(1, 29)"))


if __name__ == "__main__":
    unittest.main()
