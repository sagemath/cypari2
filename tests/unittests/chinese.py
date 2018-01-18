# -*- coding: utf-8 -*-

"""Original pari/GP test file chinese :
chinese(Mod(x,x^2+1),Mod(x,x^2+1))
chinese(Mod(x,x^2+1),Mod(x,x^2-1))
chinese(Mod(1,2)*x+Mod(1,2), Mod(2,3)*x^2+Mod(1,3)*x+Mod(1,3))
chinese([Mod(1,2),Mod(1,3)], [Mod(1,4),Mod(1,2)])
chinese(1)
chinese([])
chinese(Mod(1+x,x^2),Mod(0,1))
chinese(Mod(1+x,x^2),Mod(1,2))
chinese(Mod(0,1),Mod(1+x,x^2))

"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestChinese(unittest.TestCase):
    def test_chinese(self):
        self.assertEquals(pari.chinese(pari.Mod('x', 'x^2+1'), pari.Mod('x', 'x^2+1')), 'Mod(x, x^2 + 1)')
        self.assertEquals(pari.chinese(pari.Mod('x', 'x^2+1'), pari.Mod('x', 'x^2-1')), 'Mod(x, x^4 - 1)')
        self.assertEquals(str(pari.chinese(pari.Mod(1, 2) * 'x' + pari.Mod(1, 2),
                                       pari.Mod(2, 3) * 'x^2' + pari.Mod(1, 3) * 'x' + pari.Mod(1, 3))),
                          'Mod(2, 3)*x^2 + Mod(1, 6)*x + Mod(1, 6)')
        self.assertEquals(pari.chinese([pari.Mod(1, 2), pari.Mod(1, 3)], [pari.Mod(1, 4), pari.Mod(1, 2)]),
                          '[Mod(1, 4), Mod(1, 6)]')
        with self.assertRaises(PariError) as context:
            pari.chinese(1)
        self.assertTrue('incorrect type in association (t_INT)' in str(context.exception))
        self.assertEquals(pari.chinese([]), 'Mod(0, 1)')
        self.assertEquals(pari.chinese(pari.Mod('1+x', 'x^2'), pari.Mod(0, 1)), 'Mod(x + 1, x^2)')
        self.assertEquals(pari.chinese(pari.Mod('1+x', 'x^2'), pari.Mod(1, 2)), 'Mod(x + 1, 2*x^2)')
        self.assertEquals(pari.chinese(pari.Mod(0, 1), pari.Mod('1+x', 'x^2')), 'Mod(x + 1, x^2)')
        

"""**** Original expected results ****

Mod(x, x^2 + 1)
Mod(x, x^4 - 1)
Mod(2, 3)*x^2 + Mod(1, 6)*x + Mod(1, 6)
[Mod(1, 4), Mod(1, 6)]
  ***   at top-level: chinese(1)
  ***                 ^----------
  *** chinese: incorrect type in association (t_INT).
Mod(0, 1)
Mod(x + 1, x^2)
Mod(x + 1, 2*x^2)
Mod(x + 1, x^2)

"""
