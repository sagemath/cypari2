# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file qfbclassno :
qfbclassno(-44507759)
qfbclassno(-57403799)
qfbclassno(-94361767)
qfbclassno(-111385627)
qfbclassno(-136801204)
qfbclassno(-185415288)
qfbclassno(-198154147)
qfbclassno(-223045972)
qfbclassno(-1253840791)
qfbclassno(-1382998299)
qfbclassno(-1567139127)
qfbclassno(-1788799151)
qfbclassno(-1850979435)
qfbclassno(-4386842803)
qfbclassno(-5082406399)
qfbclassno(1-2^100)
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestQfbclassno(unittest.TestCase):
    def test_qfbclassno(self):
        self.assertEquals(pari.qfbclassno(-44507759), '10125')
        self.assertEquals(pari.qfbclassno(-57403799), '11045')
        self.assertEquals(pari.qfbclassno(-94361767), '4802')
        self.assertEquals(pari.qfbclassno(-111385627), '1660')
        self.assertEquals(pari.qfbclassno(-136801204), '2136')
        self.assertEquals(pari.qfbclassno(-185415288), '2144')
        self.assertEquals(pari.qfbclassno(-198154147), '1508')
        self.assertEquals(pari.qfbclassno(-223045972), '2728')
        self.assertEquals(pari.qfbclassno(-1253840791), '15376')
        self.assertEquals(pari.qfbclassno(-1382998299), '7688')
        self.assertEquals(pari.qfbclassno(-1567139127), '15376')
        self.assertEquals(pari.qfbclassno(-1788799151), '76800')
        self.assertEquals(pari.qfbclassno(-1850979435), '7688')
        self.assertEquals(pari.qfbclassno(-4386842803), '8112')
        self.assertEquals(pari.qfbclassno(-5082406399), '32448')
        self.assertEquals(pari.qfbclassno(1-int(pow(2, 100))), '641278838681600')

"""**** Original expected results ****

10125
11045
4802
1660
2136
2144
1508
2728
15376
7688
15376
76800
7688
8112
32448
641278838681600

"""
