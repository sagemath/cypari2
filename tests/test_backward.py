#!/usr/bin/env python
#*****************************************************************************
#       Copyright (C) 2020 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import cypari2
import unittest

class TestBackward(unittest.TestCase):
    def test_polisirreducible(self):
        pari = cypari2.Pari()
        p = pari('x^2 + 1')
        self.assertTrue(p.polisirreducible())

    def test_sqrtint(self):
        pari = cypari2.Pari()
        self.assertEqual(pari(10).sqrtint(), 3)

    def test_poldegree(self):
        pari = cypari2.Pari()
        self.assertEqual(pari('x + 1').poldegree(), 1)
        self.assertEqual(pari('x*y^2 + 1').poldegree(pari('x')), 1)
        self.assertEqual(pari('x*y^2 + 1').poldegree(pari('y')), 2)

if __name__ == '__main__':
    unittest.main()
