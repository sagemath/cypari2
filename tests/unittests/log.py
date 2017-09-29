# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file log :
default(realprecision,38);
log(1+10^-30)
lngamma(1+10^-30)
lngamma(10^-30)
iferr(log(2+O(33)),E,E)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestLog(unittest.TestCase):
    def test_log(self):
        oldprec = pari.set_real_precision(38)

        self.assertEquals(str(pari.log('1+10^-30', precision=127)), '9.9999999999999999999999999999950000000 E-31')
        self.assertEquals(str(pari.lngamma('1+10^-30', precision=127)), '-5.7721566490153286060651209008157996401 E-31')
        self.assertEquals(str(pari.lngamma('10^-30', precision=127)), '69.077552789821370520539743640530349012')
        with self.assertRaises(PariError) as context:
            pari.log('2+O(33)', precision=127)
        self.assertTrue('not a prime number in p-adic log: 33' in str(context.exception))

        pari.set_real_precision(oldprec)

"""**** Original expected results ****

9.9999999999999999999999999999950000000 E-31
-5.7721566490153286060651209008157996401 E-31
69.077552789821370520539743640530349012
error("not a prime number in p-adic log: 33.")

"""
