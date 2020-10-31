#!/usr/bin/env python
#*****************************************************************************
#       Copyright (C) 2020 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import random
import cypari2
import unittest

class TestPariInteger(unittest.TestCase):
    def randint(self):
        p = random.random()
        if p < 0.05:
            return random.randint(-2, 2)
        elif p < 0.5:
            return random.randint(-2**30, 2**30)
        else:
            return random.randint(-2**100, 2**100)

    def cmp(self, a, b):
        pari = cypari2.Pari()
        pa = pari(a)
        pb = pari(b)

        self.assertTrue(pa == pa and a == pa and pa == a)
        self.assertEqual(a == b, pa == pb)
        self.assertEqual(a != b, pa != pb)
        self.assertEqual(a < b, pa < pb)
        self.assertEqual(a <= b, pa <= pb)
        self.assertEqual(a > b, pa > pb)
        self.assertEqual(a >= b, pa >= pb)

    def test_cmp(self):
        for _ in range(100):
            a = self.randint()
            b = self.randint()
            self.cmp(a, a)
            self.cmp(a, b)

    def test_binop(self):
        pari = cypari2.Pari()

        for _ in range(100):
            a = self.randint()
            b = self.randint()

            self.assertEqual(a + b, pari(a) + pari(b))
            self.assertEqual(a - b, pari(a) - pari(b))
            self.assertEqual(a * b, pari(a) * pari(b))

            if b > 0:
                self.assertEqual(a % b, pari(a) % pari(b))

    def test_zero_division(self):
        pari = cypari2.Pari()
        with self.assertRaises(cypari2.PariError):
            pari(2) / pari(0)

if __name__ == '__main__':
    unittest.main()
