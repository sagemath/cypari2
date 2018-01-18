# -*- coding: utf-8 -*-

"""Original pari/GP test file lambert :
do(y)=my(x = lambertw(y)); exp(x)*x / y;
do(-1)
do(I)
default(realprecision,38);
do(2)
default(realprecision,211);
do(1e14)
do(y)=
{ my(x = lambertw(y), e = normlp(Vec(exp(x)*x - y)));
  if (e > 5e-38, error([e, y]));
}
default(realprecision,38);
do(O(x^10))
do(O(x^30))
do(3+O(x^10))
do(3+O(x^30))
do(x)
do(x+O(x^10))
do(x+O(x^30))
do(3+O(x))
do(3+x)
do(3+x+O(x^10))
do(3+x+O(x^30))
do(x^2-2*x^3)
do(x^2-2*x^3+O(x^10))
do(x^2-2*x^3+O(x^30))
do(3+x^2-2*x^3)
do(3+x^2-2*x^3+O(x^10))
do(3+x^2-2*x^3+O(x^30))
lambertw(1/x)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestLambert(unittest.TestCase):
    def test_lambert(self):
        def do(y, precision=128):
            x = pari.lambertw(y, precision=precision)
            return pari.exp(x)*x/y;
        with self.assertRaises(PariError) as context:
            do(-1)
        self.assertTrue('domain error in Lw: y < 0' in str(context.exception))
        with self.assertRaises(PariError) as context:
            do('I')
        self.assertTrue('sorry, lambert(t_COMPLEX) is not yet implemented' in str(context.exception))
        pari.set_real_precision(38)
        self.assertEquals(do(2), '1.0000000000000000000000000000000000000')
        pari.set_real_precision(211)
        self.assertEquals(do('1e14', precision=701),
                          '0.9999999999999999999999999999999999999999999999999999999999999999999' +
                          '999999999999999999999999999999999999999999999999999999999999999999999999999999999' +
                          '999999999999999999999999999999999999999999999999999999999999999')

        def do2(y, precision=128):
            x = pari.lambertw(y, precision=precision)
            e = pari.normlp(pari.Vec(pari.exp(x)*x - y))
            self.assertLessEqual(e, 5e-38)

        pari.set_real_precision(38)
        do2('O(x^10)')
        do2('O(x^30)')
        do2('3+O(x^10)')
        do2('3+O(x^30)')
        do2('x')
        do2('x+O(x^10)')
        do2('x+O(x^30)')
        do2('3+O(x)')
        do2('3+x')
        do2('3+x+O(x^10)')
        do2('3+x+O(x^30)')
        do2('x^2-2*x^3')
        do2('x^2-2*x^3+O(x^10)')
        do2('x^2-2*x^3+O(x^30)')
        do2('3+x^2-2*x^3')
        do2('3+x^2-2*x^3+O(x^10)')
        do2('3+x^2-2*x^3+O(x^30)')
        with self.assertRaises(PariError) as context:
            pari.lambertw('1/x')
        self.assertTrue('domain error in lambertw: valuation < 0' in str(context.exception))

"""**** Original expected results ****

  ***   at top-level: do(-1)
  ***                 ^------
  ***   in function do: my(x=lambertw(y));exp(x)*
  ***                        ^--------------------
  *** lambertw: domain error in Lw: y < 0
  ***   at top-level: do(I)
  ***                 ^-----
  ***   in function do: my(x=lambertw(y));exp(x)*
  ***                        ^--------------------
  *** lambertw: sorry, lambert(t_COMPLEX) is not yet implemented.
1.0000000000000000000000000000000000000
0.99999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999999999999999999
9999999999999999999999999999999999999999999999999999999999999
  ***   at top-level: lambertw(1/x)
  ***                 ^-------------
  *** lambertw: domain error in lambertw: valuation < 0

"""
