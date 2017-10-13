# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file charpoly :
charpoly([x,x+1;1,2],y,0)
charpoly([x,x+1;1,2],y,1)
charpoly([x,x+1;1,2],y,2)
charpoly([x,x+1;1,2],y,3)
charpoly([0,0,2,2;0,0,2,2;2,2,0,0;2,2,0,0])
charpoly([0,0,2,2;0,0,2,2;2,2,0,0;2,2,0,0],,4)
minpoly(matrix(4,4,i,j,i/j))

default(realprecision,38);
A=[5/3,7/45;0,21/10];
mateigen(A)
mateigen(A*1.)
mateigen(A,1)
M=[x,x+y;x+1,1];charpoly(M,w)
v=[1,1.,Mod(1,3),1/2,1+O(3),I,quadgen(5),matid(2)*Mod(1,3),matid(2)*Mod(1,2^64+13)];
for(i=1,#v,print(charpoly(v[i])))
charpoly(matid(4),,0)
charpoly(matid(4),,3)
charpoly(matid(4)*(2^64+13))
m=[1,2,3,4;5,6,7,8;9,10,11,12;1,5,7,11];
charpoly(m*Mod(1,3))
charpoly(m*Mod(1,2^64+13))
matadjoint(matid(2),1)
matadjoint([;])
matadjoint(Mat(1))
matadjoint([x,0,0;0,0,0;0,0,0])
matadjoint([Mod(1,2)*x,0,0;0,0,0;0,0,0])
charpoly(x*matid(3))
minpoly(Mod(x+1,x^4+1))
minpoly(Mod(x,x^2))
minpoly(Mod(1,x^2+x+1))
minpoly(Mod(1,x^24+1))

a=[1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0;0,1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0;0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0;-1,-1,-1,4,0,0,0,0,-1,0,0,0,0,0,0,0,0;0,0,0,0,1,0,0,-1,0,0,0,0,0,0,0,0,0;0,0,0,0,0,1,0,-1,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0;0,0,0,0,-1,-1,-1,4,-1,0,0,0,0,0,0,0,0;0,0,0,-1,0,0,0,-1,4,-1,-1,0,0,0,0,0,0;0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0,0;0,0,0,0,0,0,0,0,-1,0,4,-1,-1,-1,0,0,0;0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0;0,0,0,0,0,0,0,0,0,0,-1,0,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0,-1,0,0,3,-1,0,-1;0,0,0,0,0,0,0,0,0,0,0,0,0,-1,3,-2,0;0,0,0,0,0,0,0,0,0,0,0,0,0,0,-2,2,0;0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,1];
mateigen(a);
mateigen([;])
mateigen([;],1)
mateigen(Mat(1))
mateigen(Mat(1),1)

\\ Errors, keep at end of file
charpoly(Mod('b, 'b^2 + Mod('a,'a^2+1)), 'newvar)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestCharpoly(unittest.TestCase):
    def setUp(self):
        pari.set_real_precision(38)

    def tearDown(self):
        pari.set_real_precision(15)

    def test_charpoly(self):
        x = pari('x')
        y = pari('y')
        self.assertEquals(pari.charpoly('[x,x+1;1,2]', y, 0), '(-y + 1)*x + (y^2 - 2*y - 1)')
        self.assertEquals(pari.charpoly('[x,x+1;1,2]', y, 1), '(-y + 1)*x + (y^2 - 2*y - 1)')
        self.assertEquals(pari.charpoly('[x,x+1;1,2]', y, 2), '(-y + 1)*x + (y^2 - 2*y - 1)')
        self.assertEquals(pari.charpoly('[x,x+1;1,2]', y, 3), '(-y + 1)*x + (y^2 - 2*y - 1)')
        self.assertEquals(pari.charpoly('[0,0,2,2;0,0,2,2;2,2,0,0;2,2,0,0]'), 'x^4 - 16*x^2')
        self.assertEquals(pari.charpoly('[0,0,2,2;0,0,2,2;2,2,0,0;2,2,0,0]', None, 4), 'x^4 - 16*x^2')

        M = '[x,x+y;x+1,1]';
        self.assertEquals(pari.charpoly(M, pari('w')), '-x^2 + (-y - w)*x + (-y + (w^2 - w))')
        v = [1, pari('1.'), pari.Mod(1, 3), '1/2', '1+O(3)', 'I',
             pari.quadgen(5), pari.matid(2) * pari.Mod(1, 3),
             pari.matid(2) * pari.Mod(1, 2 ** 64 + 13)];

        res = ['x - 1',
               'x - 1.0000000000000000000000000000000000000',
               'x + Mod(2, 3)',
               'x - 1/2',
               'x + (2 + O(3))',
               'x^2 + 1',
               'x^2 - x - 1',
               'Mod(1, 3)*x^2 + Mod(1, 3)*x + Mod(1, 3)',
               'Mod(1, 18446744073709551629)*x^2 + Mod(18446744073709551627, 18446744073709551629)*x + Mod(1, '
               '18446744073709551629)']

        for i in range(0, len(v)):
            self.assertEquals(pari.charpoly(v[i]), res[i])
        self.assertEquals(pari.charpoly(pari.matid(4), None, 0), 'x^4 - 4*x^3 + 6*x^2 - 4*x + 1')
        self.assertEquals(pari.charpoly(pari.matid(4), None, 3), 'x^4 - 4*x^3 + 6*x^2 - 4*x + 1')
        self.assertEquals(pari.charpoly(pari.matid(4) * (2 ** 64 + 13)),
                          'x^4 - 73786976294838206516*x^3 + 2041694201525630783657939720089299321846*x^2 - '
                          '25108406941546723108427206932497066002105857518694949724756*x + '
                          '115792089237316195749980275248795307917777354730270819790751905975615430356881'
                          )
        m = pari('[1,2,3,4;5,6,7,8;9,10,11,12;1,5,7,11]');
        self.assertEquals(pari.charpoly(m * pari.Mod(1, 3)),
                          'Mod(1, 3)*x^4 + Mod(1, 3)*x^3 + Mod(1, 3)*x^2 + Mod(1, 3)*x')
        self.assertEquals(pari.charpoly(m * pari.Mod(1, 2 ** 64 + 13)),
                          'Mod(1, 18446744073709551629)*x^4 + Mod(18446744073709551600, 18446744073709551629)*x^3 + '
                          'Mod(46, 18446744073709551629)*x^2 + Mod(16, 18446744073709551629)*x')
        with self.assertRaises(PariError) as context:
            pari.charpoly(x * pari.matid(3))
        self.assertTrue('incorrect priority in charpoly: variable x = x' in str(context.exception))

    def test_matadjoint(self):
        self.assertEquals(pari.matadjoint(pari.matid(2), 1), '[1, 0; 0, 1]')
        self.assertEquals(pari.matadjoint('[;]'), '[;]')
        self.assertEquals(pari.matadjoint(pari.Mat(1)), 'Mat(1)')
        self.assertEquals(pari.matadjoint('[x,0,0;0,0,0;0,0,0]'), '[0, 0, 0; 0, 0, 0; 0, 0, 0]')
        self.assertEquals(pari.matadjoint('[Mod(1,2)*x,0,0;0,0,0;0,0,0]'),
                          '[Mod(0, 2), Mod(0, 2), Mod(0, 2); Mod(0, 2), Mod(0, 2), Mod(0, 2)'
                          '; Mod(0, 2), Mod(0, 2), Mod(0, 2)]')

    def test_minpoly(self):
        x = pari('x')
        self.assertEquals(pari.minpoly(pari.Mod(x + 1, x ** 4 + 1)), 'x^4 - 4*x^3 + 6*x^2 - 4*x + 2')
        self.assertEquals(pari.minpoly(pari.Mod(x, x ** 2)), 'x^2')
        self.assertEquals(pari.minpoly(pari.Mod(1, x ** 2 + x + 1)), 'x - 1')
        self.assertEquals(pari.minpoly(pari.Mod(1, x ** 24 + 1)), 'x - 1')

    def test_mateigen(self):
        A = '[5/3,7/45;0,21/10]';
        self.assertEquals(pari.mateigen(A), '[1, 14/39; 0, 1]')
        self.assertEquals(str(pari.mateigen(A * pari('1.'), precision=128)),
                          '[1, 0.35897435897435897435897435897435897438; 0, 1]')
        self.assertEquals(pari.mateigen(A, 1), '[[5/3, 21/10], [1, 14/39; 0, 1]]')

        a = ('[1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0;0,1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0;0,0,1,-1,0,0,0,0,'
             '0,0,0,0,0,0,0,0,0;-1,-1,-1,4,0,0,0,0,-1,0,0,0,0,0,0,0,0;0,0,0,0,1,0,0,-1,0,0,0,0,0,0,0,0'
             ',0;0,0,0,0,0,1,0,-1,0,0,0,0,0,0,0,0,0;0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0;0,0,0,0,-1,-1,-'
             '1,4,-1,0,0,0,0,0,0,0,0;0,0,0,-1,0,0,0,-1,4,-1,-1,0,0,0,0,0,0;0,0,0,0,0,0,0,0,-1,1,0,0,0,'
             '0,0,0,0;0,0,0,0,0,0,0,0,-1,0,4,-1,-1,-1,0,0,0;0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0;0,0,0,0'
             ',0,0,0,0,0,0,-1,0,1,0,0,0,0;0,0,0,0,0,0,0,0,0,0,-1,0,0,3,-1,0,-1;0,0,0,0,0,0,0,0,0,0,0,0'
             ',0,-1,3,-2,0;0,0,0,0,0,0,0,0,0,0,0,0,0,0,-2,2,0;0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,1]')

        pari.mateigen(a, precision=128)
        self.assertEquals(pari.mateigen('[;]', precision=128), '[]')
        self.assertEquals(pari.mateigen('[;]', 1, precision=128), '[[], [;]]')
        self.assertEquals(pari.mateigen(pari.Mat(1), precision=128), 'Mat(1)')
        self.assertEquals(pari.mateigen(pari.Mat(1), 1, precision=128), '[[1], Mat(1)]')
"""**** Original expected results ****

(-y + 1)*x + (y^2 - 2*y - 1)
(-y + 1)*x + (y^2 - 2*y - 1)
(-y + 1)*x + (y^2 - 2*y - 1)
(-y + 1)*x + (y^2 - 2*y - 1)
x^4 - 16*x^2
x^4 - 16*x^2
x^2 - 4*x

[1 14/39]

[0     1]


[1 0.35897435897435897435897435897435897438]

[0                                        1]

[[5/3, 21/10], [1, 14/39; 0, 1]]
-x^2 + (-y - w)*x + (-y + (w^2 - w))
x - 1
x - 1.0000000000000000000000000000000000000
x + Mod(2, 3)
x - 1/2
x + (2 + O(3))
x^2 + 1
x^2 - x - 1
Mod(1, 3)*x^2 + Mod(1, 3)*x + Mod(1, 3)
Mod(1, 18446744073709551629)*x^2 + Mod(18446744073709551627, 184467440737095
51629)*x + Mod(1, 18446744073709551629)
x^4 - 4*x^3 + 6*x^2 - 4*x + 1
x^4 - 4*x^3 + 6*x^2 - 4*x + 1
x^4 - 73786976294838206516*x^3 + 2041694201525630783657939720089299321846*x^
2 - 25108406941546723108427206932497066002105857518694949724756*x + 11579208
9237316195749980275248795307917777354730270819790751905975615430356881
Mod(1, 3)*x^4 + Mod(1, 3)*x^3 + Mod(1, 3)*x^2 + Mod(1, 3)*x
Mod(1, 18446744073709551629)*x^4 + Mod(18446744073709551600, 184467440737095
51629)*x^3 + Mod(46, 18446744073709551629)*x^2 + Mod(16, 1844674407370955162
9)*x

[1 0]

[0 1]

[;]

[1]


[0 0 0]

[0 0 0]

[0 0 0]


[Mod(0, 2) Mod(0, 2) Mod(0, 2)]

[Mod(0, 2) Mod(0, 2) Mod(0, 2)]

[Mod(0, 2) Mod(0, 2) Mod(0, 2)]

  ***   at top-level: charpoly(x*matid(3))
  ***                 ^--------------------
  *** charpoly: incorrect priority in charpoly: variable x = x
x^4 - 4*x^3 + 6*x^2 - 4*x + 2
x^2
x - 1
x - 1
[]
[[], [;]]

[1]

[[1], Mat(1)]
  ***   at top-level: charpoly(Mod('b,'b^2
  ***                 ^--------------------
  *** charpoly: incorrect priority in RgXQ_charpoly: variable newvar < a

"""
