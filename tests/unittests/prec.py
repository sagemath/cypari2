# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file prec :
precision(0)
bitprecision(0)
precision(I,3)
default(realprecision,38);
t=(precision(1.,77)*x+1);
precision(t)
localprec(57);precision(1.)
localbitprec(128);bitprecision(1.)
bitprecision(1 + O(x), 10)
bitprecision(1 + O(3^5), 10)
bitprecision(1, 10)
precision(1./t)
precision(Qfb(1,0,-2));

serprec(1,x)
serprec(x+O(x^3),x)
serprec(x+O(x^3),y)
serprec((1+O(y^2))*x+y + O(y^3), y)

padicprec(0,2)
padicprec(0,"")
padicprec(1,2)  == padicprec(0,2)
padicprec(1/2,2)== padicprec(0,2)
padicprec(Mod(1,9),3)
padicprec(O(2^2),3)
padicprec(O(2^2),2)
t=1+O(2^3);
padicprec(t,2)
padicprec((x+2)*t, 2)
padicprec((1+2*x+O(x^2))*t, 2)
padicprec([2,4]*t, 2)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestPrec(unittest.TestCase):
    def test_prec(self):
        self.assertEquals(pari.precision(0), '+oo')
        self.assertEquals(pari.bitprecision(0), '+oo')
        self.assertEquals(pari.precision('I', 3), 'I')
        pari.set_real_precision(38)
        t = pari('precision(1.,77)*x+1');
        self.assertEquals(pari.precision(t), '77')
        pari.localprec(57);
        self.assertEquals(pari.precision('1.'), '57')
        pari.localbitprec(128);
        self.assertEquals(pari.bitprecision('1.'), '128')
        self.assertEquals(pari.bitprecision('1 + O(x)', 10), '1 + O(x)')
        self.assertEquals(pari.bitprecision('1 + O(3^5)', 10), '1 + O(3^5)')
        self.assertEquals(pari.bitprecision(1, 10), '1')
        self.assertEquals(pari.precision('1./t'), '38')
        pari.precision(pari.Qfb(1, 0, -2));

    def test_serprec(self):
        self.assertEquals(pari.serprec(1, 'x'), '+oo')
        self.assertEquals(pari.serprec('x+O(x^3)', 'x'), '3')
        self.assertEquals(pari.serprec('x+O(x^3)', 'y'), '+oo')
        self.assertEquals(pari.serprec('(1+O(y^2))*x+y + O(y^3)', 'y'), '2')

    def test_padicprec(self):
        self.assertEquals(pari.padicprec(0, 2), '+oo')
        with self.assertRaises(PariError) as context:
            pari.padicprec(0, '""')
        self.assertTrue('incorrect type in padicprec (t_STR)' in str(context.exception))
        self.assertEquals(pari.padicprec(1, 2), pari.padicprec(0, 2))
        self.assertEquals(pari.padicprec('1/2', 2), pari.padicprec(0, 2))
        self.assertEquals(pari.padicprec(pari.Mod(1, 9), 3), '2')
        with self.assertRaises(PariError) as context:
            pari.padicprec('O(2^2)', 3)
        self.assertTrue('inconsistent moduli in padicprec: 2 != 3' in str(context.exception))
        self.assertEquals(pari.padicprec('O(2^2)', 2), '2')
        t = '1+O(2^3)';
        self.assertEquals(pari.padicprec(t, 2), '3')
        self.assertEquals(pari.padicprec('(x+2)*(1+O(2^3))', 2), '3')
        self.assertEquals(pari.padicprec('(1+2*x+O(x^2))*(1+O(2^3))', 2), '3')
        self.assertEquals(pari.padicprec('[2,4]*(1+O(2^3))', 2), '4')
        pari.set_real_precision(15)
"""**** Original expected results ****

+oo
+oo
I
77
57
128
1 + O(x)
1 + O(3^5)
1
38
+oo
3
+oo
2
+oo
  ***   at top-level: padicprec(0,"")
  ***                 ^---------------
  *** padicprec: incorrect type in padicprec (t_STR).
1
1
2
  ***   at top-level: padicprec(O(2^2),3)
  ***                 ^-------------------
  *** padicprec: inconsistent moduli in padicprec: 2 != 3
2
3
3
3
4

"""
