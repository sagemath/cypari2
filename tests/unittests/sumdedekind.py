# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file sumdedekind :
sumdedekind(-2,-3)
sumdedekind(2, 4)
sumdedekind(123186,28913191)
sumdedekind(2^64+1, 2^65)
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestSumdedekind(unittest.TestCase):
    def test_sumdedekind(self):
        self.assertEquals(pari.sumdedekind(-2, -3), '-1/18')
        self.assertEquals(pari.sumdedekind(2, 4), '0')
        self.assertEquals(pari.sumdedekind(123186, 28913191), '1145846923/57826382')
        self.assertEquals(pari.sumdedekind(int(pow(2, 64)) + 1, int(pow(2, 65))),
                          '56713727820156410558782357164918483627/73786976294838206464')

"""**** Original expected results ****

-1/18
0
1145846923/57826382
56713727820156410558782357164918483627/73786976294838206464

"""
