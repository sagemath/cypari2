# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file nfrootsof1 :
allocatemem(20*10^6);
do(P)=nfrootsof1(nfinit(P))[1];

do(polcyclo(23))
do(polresultant(y^3*x^3-y^2*x^2+1, polcyclo(23)))
do(x^54+9*x^51+18*x^48-81*x^45+387*x^42-729*x^39+1953*x^36-7560*x^33+14229*x^30-12393*x^27-270*x^24+6156*x^21+26136*x^18-77679*x^15+88452*x^12-49572*x^9+10287*x^6+972*x^3+27)
do(x^2+396735)
do(x^2+4372152)
do(x^2+x+99184)
do(x^16+2*x^15-x^14-4*x^13+x^12+4*x^11-2*x^9-3*x^8+7*x^6-9*x^4+4*x^3+4*x^2-4*x+1)
do(polcyclo(68))
do(polcyclo(85))
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestNfrootsof1(unittest.TestCase):
    def test_nfrootsof1(self):
        pari.allocatemem(20*1e6);
        def do(P):
            return pari.nfrootsof1(pari.nfinit(P))[0];

        self.assertEqual(do(pari.polcyclo(23)), '46')
        self.assertEqual(do(pari.polresultant('y^3*x^3-y^2*x^2+1', pari.polcyclo(23))), '46')
        self.assertEqual(do('x^54+9*x^51+18*x^48-81*x^45+387*x^42-729*x^39+1953*x^36-7560*x^33+14229*x^30-12393*x^27-270*x^24+6156*' +
           'x^21+26136*x^18-77679*x^15+88452*x^12-49572*x^9+10287*x^6+972*x^3+27'), '18')
        self.assertEqual(do('x^2+396735'), '2')
        self.assertEqual(do('x^2+4372152'), '2')
        self.assertEqual(do('x^2+x+99184'), '2')
        self.assertEqual(do('x^16+2*x^15-x^14-4*x^13+x^12+4*x^11-2*x^9-3*x^8+7*x^6-9*x^4+4*x^3+4*x^2-4*x+1'), '4')
        self.assertEqual(do(pari.polcyclo(68)), '68')
        self.assertEqual(do(pari.polcyclo(85)), '170')

"""**** Original expected results ****

  ***   Warning: new stack size = 20000000 (19.073 Mbytes).
46
46
18
2
2
2
4
68
170

"""
