# -*- coding: utf-8 -*-

"""Original pari/GP test file ellmodulareqn :
\\package:seadata

ellmodulareqn(2)
ellmodulareqn(11)
ellmodulareqn(3,y,z)
\\ errors
ellmodulareqn(1)
ellmodulareqn(2,y,x)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestEllmodulareqn(unittest.TestCase):

    def test_ellmodulareqn(self):
        self.assertEquals(pari.ellmodulareqn(2), '[x^3 + 48*x^2 + (-y + 768)*x + 4096, 0]')
        self.assertEquals(pari.ellmodulareqn(11), '[x^12 + (-y + 744)*x^11 + 196680*x^10 + (187*y + 21354080)*x' +
                          '^9 + (506*y + 830467440)*x^8 + (-11440*y + 16875327744)*x^7 + (-57442*y + 2085649589' +
                          '76)*x^6 + (184184*y + 1678582287360)*x^5 + (1675784*y + 9031525113600)*x^4 + (186771' +
                          '2*y + 32349979904000)*x^3 + (-8252640*y + 74246810880000)*x^2 + (-19849600*y + 98997' +
                          '734400000)*x + (y^2 - 8720000*y + 58411072000000), 1]')
        self.assertEquals(pari.ellmodulareqn(3, 'y', 'z'), '[y^4 + 36*y^3 + 270*y^2 + (-z + 756)*y + 729, 0]')

    def test_ellmodulareqn_errors(self):
        with self.assertRaises(PariError) as context:
            pari.ellmodulareqn(1)
        self.assertTrue('not a prime number in ellmodulareqn (level): 1' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.ellmodulareqn(2, 'y', 'x')
        self.assertTrue('incorrect priority in ellmodulareqn: variable y >= x' in str(context.exception))

"""**** Original expected results ****

[x^3 + 48*x^2 + (-y + 768)*x + 4096, 0]
[x^12 + (-y + 744)*x^11 + 196680*x^10 + (187*y + 21354080)*x^9 + (506*y + 83
0467440)*x^8 + (-11440*y + 16875327744)*x^7 + (-57442*y + 208564958976)*x^6
 + (184184*y + 1678582287360)*x^5 + (1675784*y + 9031525113600)*x^4 + (186771
2*y + 32349979904000)*x^3 + (-8252640*y + 74246810880000)*x^2 + (-19849600*y
 + 98997734400000)*x + (y^2 - 8720000*y + 58411072000000), 1]
[y^4 + 36*y^3 + 270*y^2 + (-z + 756)*y + 729, 0]
  ***   at top-level: ellmodulareqn(1)
  ***                 ^----------------
  *** ellmodulareqn: not a prime number in ellmodulareqn (level): 1.
  ***   at top-level: ellmodulareqn(2,y,x)
  ***                 ^--------------------
  *** ellmodulareqn: incorrect priority in ellmodulareqn: variable y >= x

"""
