# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file subst :
x; y; p; q;
subst(Y/X,X,x)
substvec(x+y,[x,y],[1,x])

\\ #1321
v = [p + w*q, w*p + q] * Mod(1, w + 1);
substvec(x+y, [x, y], v)
\\ #1447
subst(O(x^2),x,0*x)
subst(x+O(x^2),x,Mod(1,3))
subst(x+O(x^2),x,Mod(0,3))
subst(1/x+O(x^2),x,Mod(0,3))
subst(2+x+O(x^2),x,Mod(0,3))
subst(Pol(0),x,Mod(1,3))
subst(Pol(0),x,Mod(1,3)*matid(2))
subst(Pol(1),x,Mod(1,3))
subst(Pol(1),x,Mod(1,3)*matid(2))

substpol(x,1/x,y)
substpol(Mod(x*y^2, y^3*x^2+1), y^2,y)
substpol(x*y^2/(y^3*x^2+1), y^2,y)
substpol(List(), y^2,y)
substpol(List(x^2*y^2), y^2,y)
substpol(x^2+y^3*x^3+O(x^4),y^2, y)

subst(1,x,[;])
subst(1,x,Mat([1,2]))
subst(x^2+x^3+O(x^4),x, 2*y+O(y^2))

substpol(1+O(x^2),x^2,x)
substpol(x^2+O(x^4),x^2,x)
substpol(x+O(x^4),x^2,x)
substpol(1,x^2,x)

\\#1727
substvec(1+x+y+x*y+O(x^2), [x,y],[x,y])

subst(Mod(1/z,y),z,x)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestSubst(unittest.TestCase):
    def test_subst(self):
        self.assertEquals(pari.subst('Y/X', 'X', 'x'), 'Y/x')
        self.assertEquals(pari.substvec('x+y', ['x', 'y'], [1, 'x']), 'x + 1')

        # #1321
        v = '[p + w*q, w*p + q] * Mod(1, w + 1)';
        self.assertEquals(pari.substvec('x+y', ['x', 'y'], v), '0')
        # #1447
        self.assertEquals(pari.subst('O(x^2)', 'x', '0*x'), 'O(x^2)')
        with self.assertRaises(PariError) as context:
            pari.subst('x+O(x^2)', 'x', pari.Mod(1, 3))
        self.assertTrue('forbidden substitution t_SER , t_INTMOD' in str(context.exception))

        self.assertEquals(pari.subst('x+O(x^2)', 'x', pari.Mod(0, 3)), 'Mod(0, 3)')

        with self.assertRaises(PariError) as context:
            pari.subst('1/x+O(x^2)', 'x', pari.Mod(0, 3))
        self.assertTrue('impossible inverse in gsubst: Mod(0, 3)' in str(context.exception))

        self.assertEquals(pari.subst('2+x+O(x^2)', 'x', pari.Mod(0, 3)), 'Mod(2, 3)')
        self.assertEquals(pari.subst(pari.Pol(0), 'x', pari.Mod(1, 3)), 'Mod(0, 3)')
        self.assertEquals(pari.subst(pari.Pol(0), 'x', 'Mod(1,3)*matid(2)'), '[Mod(0, 3), 0; 0, Mod(0, 3)]')
        self.assertEquals(pari.subst(pari.Pol(1), 'x', pari.Mod(1, 3)), 'Mod(1, 3)')
        self.assertEquals(pari.subst(pari.Pol(1), 'x', 'Mod(1,3)*matid(2)'), '[1, 0; 0, 1]')

        self.assertEquals(pari.substpol('x', '1/x', 'y'), '-1/-y')
        self.assertEquals(pari.substpol(pari.Mod('x*y^2', 'y^3*x^2+1'), 'y^2', 'y'), 'Mod(y*x, y^2*x^2 + 1)')
        self.assertEquals(pari.substpol('x*y^2/(y^3*x^2+1)', 'y^2', 'y'), 'y*x/(y^2*x^2 + 1)')
        self.assertEquals(pari.substpol(pari.List(), 'y^2', 'y'), 'List([])')
        self.assertEquals(pari.substpol(pari.List('x^2*y^2'), 'y^2', 'y'), 'List([y*x^2])')
        self.assertEquals(pari.substpol('x^2+y^3*x^3+O(x^4)', 'y^2', 'y'), 'x^2 + y^2*x^3 + O(x^4)')

        self.assertEquals(pari.subst(1, 'x', '[;]'), '[;]')
        with self.assertRaises(PariError) as context:
            pari.subst(1, 'x', pari.Mat([1, 2]))
        self.assertTrue('forbidden substitution t_INT , t_MAT (1x2)' in str(context.exception))
        self.assertEquals(pari.subst('x^2+x^3+O(x^4)', 'x', '2*y+O(y^2)'), '4*y^2 + O(y^3)')

        self.assertEquals(pari.substpol('1+O(x^2)', 'x^2', 'x'), '1 + O(x)')
        self.assertEquals(pari.substpol('x^2+O(x^4)', 'x^2', 'x'), 'x + O(x^2)')
        with self.assertRaises(PariError) as context:
            pari.substpol('x+O(x^4)', 'x^2', 'x')
        self.assertTrue('domain error in gdeflate: valuation(x) % 2 != 0' in str(context.exception))
        self.assertEquals(pari.substpol(1, 'x^2', 'x'), '1')

        # #1727
        self.assertEquals(pari.substvec('1+x+y+x*y+O(x^2)', ['x', 'y'], ['x', 'y']), '(y + 1) + (y + 1)*x + O(x^2)')

        self.assertEquals(pari.subst(pari.Mod('1/z', 'y'), 'z', 'x'), 'Mod(1, y)/(Mod(1, y)*x)')

"""**** Original expected results ****

Y/x
x + 1
0
O(x^2)
  ***   at top-level: subst(x+O(x^2),x,Mod
  ***                 ^--------------------
  *** subst: forbidden substitution t_SER , t_INTMOD.
Mod(0, 3)
  ***   at top-level: subst(1/x+O(x^2),x,M
  ***                 ^--------------------
  *** subst: impossible inverse in gsubst: Mod(0, 3).
Mod(2, 3)
Mod(0, 3)

[Mod(0, 3)         0]

[        0 Mod(0, 3)]

Mod(1, 3)

[1 0]

[0 1]

-1/-y
Mod(y*x, y^2*x^2 + 1)
y*x/(y^2*x^2 + 1)
List([])
List([y*x^2])
x^2 + y^2*x^3 + O(x^4)
[;]
  ***   at top-level: subst(1,x,Mat([1,2])
  ***                 ^--------------------
  *** subst: forbidden substitution t_INT , t_MAT (1x2).
4*y^2 + O(y^3)
1 + O(x)
x + O(x^2)
  ***   at top-level: substpol(x+O(x^4),x^
  ***                 ^--------------------
  *** substpol: domain error in gdeflate: valuation(x) % 2 != 0
1
(y + 1) + (y + 1)*x + O(x^2)
Mod(1, y)/(Mod(1, y)*x)

"""
