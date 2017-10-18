# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file ser :
default(realprecision,38);
s=x+x^2+O(x^5)
f=[atan,asin,acos,cosh,sinh,tanh,cotanh,acosh,asinh,atanh];
{
for (i=1,#f,
  print(f[i](s));
  print(f[i](O(x^5)));
  print(f[i]([Pol(1)]));
)
}
O(x^-2)
O(1/x^2)
trace(I*x+1+O(x^2))
norm(I*x+1+O(x^2))
a=Ser(vector(200,i,i));
a^2 == a*(a+1) - a \\ test RgX_mullow, RgX_sqrlow
3+O(1)
serreverse(x/2+O(x^2))
serreverse(tan(x)/2)

Ser(x+y+O(x^2),x)
Ser(x+y+O(x^2),y)
Ser("")
s = Ser(Mod(0,7))
Ser(Mod(1,7)*(x^4+x^2), x,3)
s+O(x^16)
s+Mod(1,7)
s+Mod(1,7)*x
s/x
s'
deriv(s,y)
trace(s)
round(s)
round(s,&e)
lift(s)
lift(s,x)
liftint(s)
Ser(x,, -5)
O(x^2)*0
deriv(Mod(2,4)*x^2+O(x^3))
x^3*(1+O(y^2))
Mod(1,3)*x^3*(1+O(y^2))
O(x)/2
s = O(3^2)+O(x);
s/3
s/2
s*3
(1+O(x))^2
1/(x+0.)+O(x^2)
[1==O(x), 1==O(x^0), 1==O(x^-1)]
[-1==O(x), -1==O(x^0), -1==O(x^-1)]
[2==O(x), 2==O(x^0), 2==O(x^-1)]

a=1./x+O(1);a-a
a=1/x+O(1);a-a
a=Mod(1,2)/x+O(1);a-a

subst(1+O(x),x,y)
subst(1+x+O(x^2),x,y^2)
O(1)==O(x)
O(1)==x
O(x)==1

exp(x+O(x^200))*exp(-x+O(x^200))
exp(x+O(x^200))^2==exp(2*x+O(x^200))

subst(1+x^3+O(x^6),x,x+O(x^4))
subst(1+x^2+O(x^6),x,x+O(x^3))
subst(1+x^3+x^4+O(x^6),x,x+x^2+O(x^3))

subst(x^2+O(x^3),x,0*x)
subst(x^2+O(x^3),x,Mod(0,3)*x)
subst(x^2+O(x^3),x,O(3)*x)
subst(1+x+O(x^2),x,0*x)
subst(1+x+O(x^2),x,Mod(0,3)*x)
subst(1+x+O(x^2),x,O(3)*x)

\\ Errors. Keep at end of file
subst(x^-1+O(x),x,Mod(0,3))
subst(O(x^-1),x,Mod(0,3))
subst(x^-1+O(x),x,0*x)
subst(O(x^-1),x,0*x)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestSer(unittest.TestCase):
    def test_ser(self):
        pari.set_real_precision(38)
        s = 'x+x^2+O(x^5)'
        f = [pari.atan, pari.asin, pari.acos, pari.cosh, pari.sinh, pari.tanh, pari.cotanh, pari.acosh, pari.asinh];

        res1 = ['x + x^2 - 1/3*x^3 - x^4 + O(x^5)',
                'x + x^2 + 1/6*x^3 + 1/2*x^4 + O(x^5)',
                '1.5707963267948966192313216916397514421 - x - x^2 - 1/6*x^3 - 1/2*x^4 + O(x^5)',
                '1 + 1/2*x^2 + x^3 + 13/24*x^4 + O(x^5)',
                'x + x^2 + 1/6*x^3 + 1/2*x^4 + O(x^5)',
                'x + x^2 - 1/3*x^3 - x^4 + O(x^5)',
                'x^-1 - 1 + 4/3*x - 2/3*x^2 + O(x^3)',
                '1.5707963267948966192313216916397514421*I - 1.0000000000000000000000000000000000000*I*x - '
                '1.0000000000000000000000000000000000000*I*x^2 - 0.16666666666666666666666666666666666667*I*x^3 - '
                '0.50000000000000000000000000000000000000*I*x^4 + O(x^5)',
                'x + x^2 - 1/6*x^3 - 1/2*x^4 + O(x^5)']

        res2 = ['O(x^5)',
                'O(x^5)',
                '1.5707963267948966192313216916397514421 + O(x^5)',
                '1 + O(x^5)',
                'O(x^5)',
                'O(x^5)',
                'O(x^5)',
                '1.5707963267948966192313216916397514421*I + O(x^5)',
                'O(x^5)']

        res3 = ['[0.78539816339744830961566084581987572105 + O(x^16)]',
                '[1.5707963267948966192313216916397514421 + O(x^8)]',
                '[O(x^8)]',
                '[1.5430806348152437784779056207570616826 + O(x^16)]',
                '[1.1752011936438014568823818505956008152 + O(x^16)]',
                '[0.76159415595576488811945828260479359041 + O(x^16)]',
                '[1.3130352854993313036361612469308478329 + O(x^16)]',
                '[O(x^8)]',
                '[0.88137358701954302523260932497979230903 + O(x^16)]']

        for i in range(0, len(f)):
            self.assertEquals(str(f[i](s, precision=128)), res1[i]);
            self.assertEquals(str(f[i]('O(x^5)', precision=128)), res2[i]);
            self.assertEquals(str(f[i]([pari.Pol(1)], precision=128)), res3[i]);

        self.assertEquals(str(pari.atanh(s, precision=128)), 'x + x^2 + 1/3*x^3 + x^4 + O(x^5)')
        self.assertEquals(str(pari.atanh('O(x^5)', precision=128)), 'O(x^5)')
        with self.assertRaises(PariError) as context:
            pari.atanh([pari.Pol(1)], precision=128)
        self.assertTrue('impossible inverse in div_ser: O(x^16)' in str(context.exception))
        self.assertEquals(pari.trace('I*x+1+O(x^2)'), '2 + O(x^2)')
        self.assertEquals(pari.norm('I*x+1+O(x^2)'), '1 + O(x^2)')

        self.assertEquals(pari.Ser('x+y+O(x^2)','x'), 'y + x + O(x^2)')
        self.assertEquals(pari.Ser('x+y+O(x^2)','y'), '(y + O(y^17)) + (1 + O(y^16))*x + O(x^2)')
        with self.assertRaises(PariError) as context:
            pari.Ser('""')
        self.assertTrue('incorrect type in gtoser (t_STR)' in str(context.exception))
        s = pari.Ser(pari.Mod(0,7))
        self.assertEquals(s, 'Mod(0, 7)*x^15 + O(x^16)')
        self.assertEquals(pari.Ser('Mod(1,7)*(x^4+x^2)', 'x', 3), 'Mod(1, 7)*x^2 + Mod(1, 7)*x^4 + O(x^5)')
        self.assertEquals(pari.deriv(s, 'y'), 'Mod(0, 7)*x^15 + O(x^16)')
        self.assertEquals(pari.trace(s), 'Mod(0, 7)*x^15 + O(x^16)')
        self.assertEquals(pari.lift(s), 'O(x^16)')
        self.assertEquals(pari.lift(s, 'x'), 'Mod(0, 7)*x^15 + O(x^16)')
        self.assertEquals(pari.liftint(s), 'O(x^16)')
        self.assertEquals(pari.deriv('Mod(2,4)*x^2+O(x^3)'), 'Mod(0, 4)*x + O(x^2)')

        self.assertEquals(pari.subst('1+O(x)', 'x', 'y'), '1 + O(y)')
        self.assertEquals(pari.subst('1+x+O(x^2)', 'x', 'y^2'), '1 + y^2 + O(y^4)')
        self.assertEquals(pari.subst('1+x^3+O(x^6)', 'x', 'x+O(x^4)'), '1 + x^3 + O(x^6)')
        self.assertEquals(pari.subst('1+x^2+O(x^6)', 'x', 'x+O(x^3)'), '1 + x^2 + O(x^4)')
        self.assertEquals(pari.subst('1+x^3+x^4+O(x^6)', 'x', 'x+x^2+O(x^3)'), '1 + x^3 + 4*x^4 + O(x^5)')

        self.assertEquals(pari.subst('x^2+O(x^3)', 'x', '0*x'), '0')
        self.assertEquals(pari.subst('x^2+O(x^3)', 'x', 'Mod(0,3)*x'), 'Mod(0, 3)')
        self.assertEquals(pari.subst('x^2+O(x^3)', 'x', 'O(3)*x'), 'O(3^2)*x^2 + O(x^3)')
        self.assertEquals(pari.subst('1+x+O(x^2)', 'x', '0*x'), '1')
        self.assertEquals(pari.subst('1+x+O(x^2)', 'x', 'Mod(0,3)*x'), 'Mod(1, 3)')
        self.assertEquals(pari.subst('1+x+O(x^2)', 'x', 'O(3)*x'), '1 + O(3)*x + O(x^2)')

    def test_serreverse(self):
        self.assertEquals(pari.serreverse('x/2+O(x^2)'), '2*x + O(x^2)')
        self.assertEquals(pari.serreverse('tan(x)/2'), '2*x - 8/3*x^3 + 32/5*x^5 - 128/7*x^7 + 512/9*x^9 - 204'
                                                       '8/11*x^11 + 8192/13*x^13 - 32768/15*x^15 + O(x^17)')

    def test_errors(self):
        with self.assertRaises(PariError) as context:
            pari.subst('x^-1+O(x)', 'x', pari.Mod(0, 3))
        self.assertTrue('impossible inverse in gsubst: Mod(0, 3)' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.subst('O(x^-1)', 'x', pari.Mod(0, 3))
        self.assertTrue('impossible inverse in gsubst: Mod(0, 3)' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.subst('x^-1+O(x)', 'x', '0*x')
        self.assertTrue('impossible inverse in gsubst: 0' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.subst('O(x^-1)', 'x', '0*x')
        self.assertTrue('impossible inverse in gsubst: 0' in str(context.exception))





"""**** Original expected results ****

x + x^2 + O(x^5)
x + x^2 - 1/3*x^3 - x^4 + O(x^5)
O(x^5)
[0.78539816339744830961566084581987572105 + O(x^16)]
x + x^2 + 1/6*x^3 + 1/2*x^4 + O(x^5)
O(x^5)
[1.5707963267948966192313216916397514421 + O(x^8)]
1.5707963267948966192313216916397514421 - x - x^2 - 1/6*x^3 - 1/2*x^4 + O(x^
5)
1.5707963267948966192313216916397514421 + O(x^5)
[O(x^8)]
1 + 1/2*x^2 + x^3 + 13/24*x^4 + O(x^5)
1 + O(x^5)
[1.5430806348152437784779056207570616826 + O(x^16)]
x + x^2 + 1/6*x^3 + 1/2*x^4 + O(x^5)
O(x^5)
[1.1752011936438014568823818505956008152 + O(x^16)]
x + x^2 - 1/3*x^3 - x^4 + O(x^5)
O(x^5)
[0.76159415595576488811945828260479359041 + O(x^16)]
x^-1 - 1 + 4/3*x - 2/3*x^2 + O(x^3)
O(x^5)
[1.3130352854993313036361612469308478329 + O(x^16)]
1.5707963267948966192313216916397514421*I - 1.000000000000000000000000000000
0000000*I*x - 1.0000000000000000000000000000000000000*I*x^2 - 0.166666666666
66666666666666666666666667*I*x^3 - 0.50000000000000000000000000000000000000*
I*x^4 + O(x^5)
1.5707963267948966192313216916397514421*I + O(x^5)
[O(x^8)]
x + x^2 - 1/6*x^3 - 1/2*x^4 + O(x^5)
O(x^5)
[0.88137358701954302523260932497979230903 + O(x^16)]
x + x^2 + 1/3*x^3 + x^4 + O(x^5)
O(x^5)
  ***   at top-level: ...rint(f[i](O(x^5)));print(f[i]([Pol(1)]));)
  ***                                             ^-----------------
  ***   in function f: atanh
  ***                  ^-----
  *** atanh: impossible inverse in div_ser: O(x^16).
O(x^-2)
O(x^-2)
2 + O(x^2)
1 + O(x^2)
1
O(x^0)
2*x + O(x^2)
2*x - 8/3*x^3 + 32/5*x^5 - 128/7*x^7 + 512/9*x^9 - 2048/11*x^11 + 8192/13*x^
13 - 32768/15*x^15 + O(x^17)
y + x + O(x^2)
(y + O(y^17)) + (1 + O(y^16))*x + O(x^2)
  ***   at top-level: Ser("")
  ***                 ^-------
  *** Ser: incorrect type in gtoser (t_STR).
Mod(0, 7)*x^15 + O(x^16)
Mod(1, 7)*x^2 + Mod(1, 7)*x^4 + O(x^5)
Mod(0, 7)*x^15 + O(x^16)
Mod(1, 7) + O(x^16)
Mod(1, 7)*x + O(x^16)
Mod(0, 7)*x^14 + O(x^15)
Mod(0, 7)*x^14 + O(x^15)
Mod(0, 7)*x^15 + O(x^16)
Mod(0, 7)*x^15 + O(x^16)
Mod(0, 7)*x^15 + O(x^16)
Mod(0, 7)*x^15 + O(x^16)
O(x^16)
Mod(0, 7)*x^15 + O(x^16)
O(x^16)
  ***   at top-level: Ser(x,,-5)
  ***                 ^----------
  *** Ser: domain error in gtoser: precision < 0
0
Mod(0, 4)*x + O(x^2)
(1 + O(y^2))*x^3
(Mod(1, 3) + O(y^2))*x^3
O(x)
O(3) + O(x)
O(3^2) + O(x)
O(3^3) + O(x)
1 + O(x)
  *** _+_: Warning: normalizing a series with 0 leading term.
x^-1 + O(x)
[0, 1, 1]
[0, 1, 1]
[0, 1, 1]
0.E-38*x^-1 + O(x^0)
O(x^0)
Mod(0, 2)*x^-1 + O(x^0)
1 + O(y)
1 + y^2 + O(y^4)
1
1
0
1 + O(x^200)
1
1 + x^3 + O(x^6)
1 + x^2 + O(x^4)
1 + x^3 + 4*x^4 + O(x^5)
0
Mod(0, 3)
O(3^2)*x^2 + O(x^3)
1
Mod(1, 3)
1 + O(3)*x + O(x^2)
  ***   at top-level: subst(x^-1+O(x),x,Mo
  ***                 ^--------------------
  *** subst: impossible inverse in gsubst: Mod(0, 3).
  ***   at top-level: subst(O(x^-1),x,Mod(
  ***                 ^--------------------
  *** subst: impossible inverse in gsubst: Mod(0, 3).
  ***   at top-level: subst(x^-1+O(x),x,0*
  ***                 ^--------------------
  *** subst: impossible inverse in gsubst: 0.
  ***   at top-level: subst(O(x^-1),x,0*x)
  ***                 ^--------------------
  *** subst: impossible inverse in gsubst: 0.

"""
