# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file pol :
o = [Mod(0,3),y,1/y, (y^2+1)/y, [1,2,3], Vecsmall([1,2,0]), Qfb(1,2,4), Qfb(1,2,-4), y+2*y^2+O(y^4)];
{
  for (i=1,#o,
    my (v = o[i]);
    printsep(" ", Pol(v,y), Pol(v,x), Polrev(v));
    printsep(" ", Ser(v,y), Ser(v,x), Ser(v,,5));
  )
}
o = [2*x+3*y, 2+x+y+O(x^2), 2+x+y+O(y^2)];
{
  for (i=1,#o,
    my (v = o[i]);
    printsep(" ",pollead(v), pollead(v,x), pollead(v,y))
  )
}
pollead(z,y)
pollead(y,z)
polgraeffe(x^2+x+1)
polgraeffe(x^3+x+1)
polsym(2*x^4+1,4)
norm(I*x+1)
trace(I*x+1)
matcompanion(2*x^2+1)
Pol("")
serlaplace(1+x+x^2)
serlaplace(x^2+x^3)

\\#1651
f1=(x-1)/(x*x-x);
type(subst(1/f1,x,1))

\\#1690
default(realprecision,38);
P(x,y)=(x+1)*y^2+(x^2-x+1)*y+(x^2+x);
polroots(P(exp(I*Pi),y))
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestPol(unittest.TestCase):
    def test_pol(self):
        o = [pari.Mod(0,3), 'y', '1/y', '(y^2+1)/y', [1,2,3], pari.Vecsmall([1,2,0]),
             pari.Qfb(1,2,4), pari.Qfb(1,2,-4), 'y+2*y^2+O(y^4)'];
        res_pol =['Mod(0, 3) Mod(0, 3) Mod(0, 3)',
                  'y x x',
                  '0 0 0',
                  'y x x',
                  'y^2 + 2*y + 3 x^2 + 2*x + 3 3*x^2 + 2*x + 1',
                  'y^2 + 2*y x^2 + 2*x 2*x + 1',
                  'y^2 + 2*y + 4 x^2 + 2*x + 4 4*x^2 + 2*x + 1',
                  'y^2 + 2*y - 4 x^2 + 2*x - 4 -4*x^2 + 2*x + 1',
                  '2*y^2 + y 2*x^2 + x 2*x^2 + x']

        res_ser = ['Mod(0, 3)*y^15 + O(y^16) Mod(0, 3)*x^15 + O(x^16) Mod(0, 3)*x^4 + O(x^5)',
                   'y + O(y^17) y + O(x^16) y + O(x^5)',
                   'y^-1 + O(y^15) 1/y + O(x^16) 1/y + O(x^5)',
                   'y^-1 + y + O(y^15) ((y^2 + 1)/y) + O(x^16) ((y^2 + 1)/y) + O(x^5)',
                   '1 + 2*y + 3*y^2 + O(y^3) 1 + 2*x + 3*x^2 + O(x^3) 1 + 2*x + 3*x^2 + O(x^3)',
                   '1 + 2*y + O(y^3) 1 + 2*x + O(x^3) 1 + 2*x + O(x^3)',
                   '1 + 2*y + 4*y^2 + O(y^3) 1 + 2*x + 4*x^2 + O(x^3) 1 + 2*x + 4*x^2 + O(x^3)',
                   '1 + 2*y - 4*y^2 + O(y^3) 1 + 2*x - 4*x^2 + O(x^3) 1 + 2*x - 4*x^2 + O(x^3)',
                   'y + 2*y^2 + O(y^4) (y + 2*y^2 + O(y^4)) + O(x^16) (y + 2*y^2 + O(y^4)) + O(x^5)']

        for i in range(0, len(o)):
            v = o[i]
            self.assertEquals('%s %s %s' % (pari.Pol(v, 'y'), pari.Pol(v, 'x'), pari.Polrev(v)), res_pol[i])
            self.assertEquals('%s %s %s' % (pari.Ser(v, 'y'), pari.Ser(v, 'x'), pari.Ser(v, None, 5)), res_ser[i])

        self.assertEquals(pari.polsym('2*x^4+1', 4), '[4, 0, 0, 0, -2]~')
        self.assertEquals(pari.norm('I*x+1'), 'x^2 + 1')
        self.assertEquals(pari.trace('I*x+1'), '2')
        self.assertEquals(pari.matcompanion('2*x^2+1'), '[0, -1/2; 1, 0]')
        with self.assertRaises(PariError) as context:
            pari.Pol('""')
        self.assertTrue('incorrect type in gtopoly (t_STR)' in str(context.exception))
        # #1651
        self.assertEquals(pari.type(pari.subst('1/((x-1)/(x*x-x))', 'x', 1)), '"t_INT"')

        # #1690
        # pari.set_real_precision(38)
        # P(x,y)=(x+1)*y^2+(x^2-x+1)*y+(x^2+x);
        # pari.polroots(P(pari.exp(I*Pi),y))
        # pari.set_real_precision(15)

    def test_pollead(self):
        o = ['2*x+3*y', '2+x+y+O(x^2)', '2+x+y+O(y^2)'];
        res_pollead = ['2 2 3', 'y + 2 y + 2 x + 2', '1 1 x + 2']
        for i in range(0, len(o)):
            v = o[i]
            self.assertEquals('%s %s %s' % (pari.pollead(v), pari.pollead(v,'x'), pari.pollead(v,'y')), res_pollead[i])

        self.assertEquals(pari.pollead('z', 'y'), 'z')
        self.assertEquals(pari.pollead('y', 'z'), 'y')

    def test_polgraeffe(self):
        self.assertEquals(pari.polgraeffe('x^2+x+1'), 'x^2 + x + 1')
        self.assertEquals(pari.polgraeffe('x^3+x+1'), '-x^3 - 2*x^2 - x + 1')

    def test_serplace(self):
        self.assertEquals(pari.serlaplace('1+x+x^2'), '2*x^2 + x + 1')
        self.assertEquals(pari.serlaplace('x^2+x^3'), '6*x^3 + 2*x^2')

"""**** Original expected results ****

Mod(0, 3) Mod(0, 3) Mod(0, 3)
Mod(0, 3)*y^15 + O(y^16) Mod(0, 3)*x^15 + O(x^16) Mod(0, 3)*x^4 + O(x^5)
y x x
y + O(y^17) y + O(x^16) y + O(x^5)
0 0 0
y^-1 + O(y^15) 1/y + O(x^16) 1/y + O(x^5)
y x x
y^-1 + y + O(y^15) ((y^2 + 1)/y) + O(x^16) ((y^2 + 1)/y) + O(x^5)
y^2 + 2*y + 3 x^2 + 2*x + 3 3*x^2 + 2*x + 1
1 + 2*y + 3*y^2 + O(y^3) 1 + 2*x + 3*x^2 + O(x^3) 1 + 2*x + 3*x^2 + O(x^3)
y^2 + 2*y x^2 + 2*x 2*x + 1
1 + 2*y + O(y^3) 1 + 2*x + O(x^3) 1 + 2*x + O(x^3)
y^2 + 2*y + 4 x^2 + 2*x + 4 4*x^2 + 2*x + 1
1 + 2*y + 4*y^2 + O(y^3) 1 + 2*x + 4*x^2 + O(x^3) 1 + 2*x + 4*x^2 + O(x^3)
y^2 + 2*y - 4 x^2 + 2*x - 4 -4*x^2 + 2*x + 1
1 + 2*y - 4*y^2 + O(y^3) 1 + 2*x - 4*x^2 + O(x^3) 1 + 2*x - 4*x^2 + O(x^3)
2*y^2 + y 2*x^2 + x 2*x^2 + x
y + 2*y^2 + O(y^4) (y + 2*y^2 + O(y^4)) + O(x^16) (y + 2*y^2 + O(y^4)) + O(x
^5)
2 2 3
y + 2 y + 2 x + 2
1 1 x + 2
z
y
x^2 + x + 1
-x^3 - 2*x^2 - x + 1
[4, 0, 0, 0, -2]~
x^2 + 1
2

[0 -1/2]

[1    0]

  ***   at top-level: Pol("")
  ***                 ^-------
  *** Pol: incorrect type in gtopoly (t_STR).
2*x^2 + x + 1
6*x^3 + 2*x^2
"t_INT"
  *** polroots: Warning: normalizing a polynomial with 0 leading term.
[0.E-38 + 0.E-38*I]~

"""
