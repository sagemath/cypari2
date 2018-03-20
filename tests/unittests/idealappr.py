# -*- coding: utf-8 -*-

"""Original pari/GP test file idealappr :
idealaddtoone(nfinit(x),[1,[;]]);
K=nfinit(x^2+23); A=idealhnf(K,x/2);
idealtwoelt(K, 3, 6)
idealtwoelt(K, A)
idealtwoelt(K, A, x)
idealtwoelt(K, [;])
idealtwoelt(K, [;], 1)
idealtwoelt(K, [;], 0)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestIdealappr(unittest.TestCase):
    def test_idealappr(self):
        pari.idealaddtoone(pari.nfinit('x'),'[1,[;]]');
        K=pari.nfinit('x^2+23'); A=pari.idealhnf(K,'x/2');

        self.assertEquals(str(pari.idealtwoelt(K, 3, 6)), '3')
        self.assertEquals(str(pari.idealtwoelt(K, A)), '[23/2, [6, 1/2]~]')
        self.assertEquals(str(pari.idealtwoelt(K, A, 'x')), '-23/2')
        self.assertEquals(str(pari.idealtwoelt(K, '[;]')), '[0, 0]')
        with self.assertRaises(PariError) as context:
            pari.idealtwoelt(K, '[;]', 1)
        self.assertTrue('domain error in idealtwoelt2: element mod ideal != 0' in str(context.exception))
        self.assertEquals(str(pari.idealtwoelt(K, '[;]', 0)), '0')

"""**** Original expected results ****

3
[23/2, [6, 1/2]~]
-23/2
[0, 0]
  ***   at top-level: idealtwoelt(K,[;],1)
  ***                 ^--------------------
  *** idealtwoelt: domain error in idealtwoelt2: element mod ideal != 0
0

"""
