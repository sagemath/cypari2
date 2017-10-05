# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file sumformal :
sumformal(1/n)
sumformal(0)
sumformal(1)
sumformal(n)
sumformal(n^2)
sumformal(x*y + 1)
sumformal(x*y + 1,y)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestSumformal(unittest.TestCase):
    def test_sumformal(self):
        with self.assertRaises(PariError) as context:
            pari.sumformal('1/n')
        self.assertTrue('incorrect type in sumformal [not a t_POL] (t_RFRAC)' in str(context.exception))
        self.assertEquals(pari.sumformal(0), '0')
        self.assertEquals(pari.sumformal(1), 'x')
        self.assertEquals(pari.sumformal('n'), '1/2*n^2 + 1/2*n')
        self.assertEquals(pari.sumformal('n^2'), '1/3*n^3 + 1/2*n^2 + 1/6*n')
        self.assertEquals(pari.sumformal('x*y + 1'), '1/2*y*x^2 + (1/2*y + 1)*x')
        self.assertEquals(pari.sumformal('x*y + 1', 'y'), '(1/2*y^2 + 1/2*y)*x + y')

"""**** Original expected results ****

  ***   at top-level: sumformal(1/n)
  ***                 ^--------------
  *** sumformal: incorrect type in sumformal [not a t_POL] (t_RFRAC).
0
x
1/2*n^2 + 1/2*n
1/3*n^3 + 1/2*n^2 + 1/6*n
1/2*y*x^2 + (1/2*y + 1)*x
(1/2*y^2 + 1/2*y)*x + y

"""
