# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file modfun :
default(realprecision,38)
eta(2+O(2^20))
eta(x+x^2+x^3+x^4+O(x^5))
eta(I)
ellj(2+O(2^20))
ellj(x+x^2+x^3+x^4+O(x^5))
theta(1/2,I)
weber(1.0*I,1)
weber(1+I)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestModfun(unittest.TestCase):
    def setUp(self):
        pari.set_real_precision(38)

    def tearDown(self):
        pari.set_real_precision(15)

    def test_eta(self):
        self.assertEqual(pari.eta('2+O(2^20)'),
                         '1 + 2 + 2^3 + 2^4 + 2^7 + 2^12 + 2^13 + 2^14 + 2^16 + 2^17 + 2^18 + 2^19 + O(2^20)')
        self.assertEqual(pari.eta('x+x^2+x^3+x^4+O(x^5)'), '1 - x - 2*x^2 - 3*x^3 - 4*x^4 + O(x^5)')
        self.assertEqual(str(pari.eta('I', precision=128)), '0.99812906992595851327996232224527387813')

    def test_ellj(self):
        self.assertEqual(pari.ellj('2+O(2^20)'), '2^-1 + 2^5 + 2^7 + 2^8 + 2^10 + 2^12 + 2^16 + O(2^18)')
        self.assertEqual(pari.ellj('x+x^2+x^3+x^4+O(x^5)'), 'x^-1 + 743 + 196884*x + 21690644*x^2 + O(x^3)')

    def test_theta(self):
        self.assertEqual(str(pari.theta('1/2', 'I', precision=128)),
                         '0.E-38 - 0.50432357748832834893222560519660217759*I')

    def test_weber(self):
        self.assertEqual(str(pari.weber('1.0*I', 1, precision=128)), '1.0905077326652576592070106557607079790')
        self.assertEqual(str(pari.weber('1+I', precision=128)),
                         '1.0811782878393746833655992417658285836 - 0.14233982193131805512395869109512286588*I')

"""**** Original expected results ****

1 + 2 + 2^3 + 2^4 + 2^7 + 2^12 + 2^13 + 2^14 + 2^16 + 2^17 + 2^18 + 2^19 + O
(2^20)
1 - x - 2*x^2 - 3*x^3 - 4*x^4 + O(x^5)
0.99812906992595851327996232224527387813
2^-1 + 2^5 + 2^7 + 2^8 + 2^10 + 2^12 + 2^16 + O(2^18)
x^-1 + 743 + 196884*x + 21690644*x^2 + O(x^3)
0.E-38 - 0.50432357748832834893222560519660217759*I
1.0905077326652576592070106557607079790
1.0811782878393746833655992417658285836 - 0.14233982193131805512395869109512
286588*I

"""
