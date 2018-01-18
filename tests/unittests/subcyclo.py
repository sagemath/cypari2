# -*- coding: utf-8 -*-

"""Original pari/GP test file subcyclo :
polsubcyclo(8,1)
polsubcyclo(1048,2)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestSubcyclo(unittest.TestCase):
    def test_subcyclo(self):
        self.assertEquals(pari.polsubcyclo(8,1), '[x - 1]')
        self.assertEquals(pari.polsubcyclo(1048,2), '[x^2 + 2, x^2 + 262, x^2 - 262, x^2 - 2, x^2 - 131, x^2 + 1, x' +
                          '^2 + x + 33]')

"""**** Original expected results ****

x - 1
[x^2 + 2, x^2 + 262, x^2 - 262, x^2 - 2, x^2 - 131, x^2 + 1, x^2 + x + 33]

"""
