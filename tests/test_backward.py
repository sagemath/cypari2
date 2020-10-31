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

    def test_nfbasis(self):
        pari = cypari2.Pari()
        x = pari('x')
        third = pari('1/3')
        self.assertEqual(pari(x**3 - 17).nfbasis(), [1, x, third*x**2 - third*x + third])

        p = pari(10**10).nextprime()
        q = (p+1).nextprime()
        x = pari('x')
        f = x**2 + p**2*q
        # Correct result
        frac = pari('1/10000000019')
        self.assertEqual(pari(f).nfbasis(), [1, frac*x])

        # Wrong result
        self.assertEqual(pari.nfbasis([f,1]), [1, x])
        # Check primes up to 10^6: wrong result
        self.assertEqual(pari.nfbasis([f, 10**6]), [1, x])
        # Correct result and faster
        self.assertEqual(pari.nfbasis([f, pari("[2,2; %s,2]"%p)]), [1, frac*x])
        # Equivalent with the above
        self.assertEqual(pari.nfbasis([f, [2,p]]), [1, frac*x])

if __name__ == '__main__':
    unittest.main()
