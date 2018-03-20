# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file modular :
v = [2,3,2^32-1,2^64-1,10^20];
f(a,b,p)=(a*Mod(1,p)) * (b*Mod(1,p));
g(a,p)=sqr(a*Mod(1,p));
test(a,b)=
{
  for (i=1,#v,print(i, ": ", f(a,b,v[i])));
  for (i=1,#v,print(i, ": ", g(a,v[i])));
}
test(polcyclo(10),polcyclo(5));
test([1,2;3,4], [-1,2;-4,2]);
Mod(Mod(1,y),x)
Mod(Mod(1,x),y)
iferr(Mod(1,"a"),E,E)
iferr(Mod(0,0),E,E)
iferr(Mod(0,Pol(0)),E,E)
iferr(Mod(x+O(x^2), x^3), E,E)
Mod(x+O(x^2), x^2)
Mod(x+O(x^3), x^2)
Mod(Mod(x,x^3), x^2)
Mod(Mod(1,12), 9)
Mod(1/x,x^2+1)
Mod([5,6],2)
Mod(3*x,2)
Mod(x,y)
Mod(Pol(0),2)
Pol(0)*Mod(1,2)
k=100000000000000000000;
Mod(3,7)^-k
Mod(3,7)^k

\g1
a=Mod(1,2);b=Mod(1,3);
a+b
a-b
a*b
a/b
a+a
a-a
a*a
a/a
a=Mod(1,x);b=Mod(1,x+1);
a+b
a-b
a*b
a/b
a+a
a-a
a*a
a/a

\\#1652
p=436^56-35;lift(Mod(271,p)^((p-1)/2))
\\#1717
Mod(0,1)==0
Mod(0,1)==1
Mod(0,1)==-1
Mod(0,x^0)==0
Mod(0,x^0)==1
Mod(0,x^0)==-1
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestModular(unittest.TestCase):
    def test_modular(self):
        v = [2, 3, '2^32-1', '2^64-1', '10^20'];

        def f(a, b, p):
            return (a * pari.Mod(1, p)) * (b * pari.Mod(1, p))

        def g(a, p):
            return pari.sqr(a * pari.Mod(1, p));

        def test(a, b, l):
            for i in range(0, len(v)):
                self.assertEquals(str(f(a, b, v[i])), l[i])

            for i in range(0, len(v)):
                self.assertEquals(str(g(a, v[i])), l[i+len(v)])

        l = ['Mod(1, 2)*x^8 + Mod(1, 2)*x^6 + Mod(1, 2)*x^4 + Mod(1, 2)*x^2 + Mod(1, 2)',
             'Mod(1, 3)*x^8 + Mod(1, 3)*x^6 + Mod(1, 3)*x^4 + Mod(1, 3)*x^2 + Mod(1, 3)',
             'Mod(1, 4294967295)*x^8 + Mod(1, 4294967295)*x^6 + Mod(1, 4294967295)*x^4 + Mod(1, 429496' +
             '7295)*x^2 + Mod(1, 4294967295)',
             'Mod(1, 18446744073709551615)*x^8 + Mod(1, 18446744073709551615)*x^6 + Mod(1, 18446744073' +
             '709551615)*x^4 + Mod(1, 18446744073709551615)*x^2 + Mod(1, 18446744073709551615)',
             'Mod(1, 100000000000000000000)*x^8 + Mod(1, 100000000000000000000)*x^6 + Mod(1, 100000000' +
             '000000000000)*x^4 + Mod(1, 100000000000000000000)*x^2 + Mod(1, 100000000000000000000)',
             'Mod(1, 2)*x^8 + Mod(1, 2)*x^6 + Mod(1, 2)*x^4 + Mod(1, 2)*x^2 + Mod(1, 2)',
             'Mod(1, 3)*x^8 + Mod(1, 3)*x^7 + Mod(2, 3)*x^5 + Mod(2, 3)*x^4 + Mod(2, 3)*x^3 + Mod(1, 3)*x + Mod(1, 3)',
             'Mod(1, 4294967295)*x^8 + Mod(4294967293, 4294967295)*x^7 + Mod(3, 4294967295)*x^6 + Mod(' +
             '4294967291, 4294967295)*x^5 + Mod(5, 4294967295)*x^4 + Mod(4294967291, 4294967295)*x^3 +' +
             ' Mod(3, 4294967295)*x^2 + Mod(4294967293, 4294967295)*x + Mod(1, 4294967295)',
             'Mod(1, 18446744073709551615)*x^8 + Mod(18446744073709551613, 18446744073709551615)*x^7 +' +
             ' Mod(3, 18446744073709551615)*x^6 + Mod(18446744073709551611, 18446744073709551615)*x^5 ' +
             '+ Mod(5, 18446744073709551615)*x^4 + Mod(18446744073709551611, 18446744073709551615)*x^3' +
             ' + Mod(3, 18446744073709551615)*x^2 + Mod(18446744073709551613, 18446744073709551615)*x ' +
             '+ Mod(1, 18446744073709551615)',
             'Mod(1, 100000000000000000000)*x^8 + Mod(99999999999999999998, 100000000000000000000)*x^7' +
             ' + Mod(3, 100000000000000000000)*x^6 + Mod(99999999999999999996, 100000000000000000000)*' +
             'x^5 + Mod(5, 100000000000000000000)*x^4 + Mod(99999999999999999996, 10000000000000000000' +
             '0)*x^3 + Mod(3, 100000000000000000000)*x^2 + Mod(99999999999999999998, 10000000000000000' +
             '0000)*x + Mod(1, 100000000000000000000)']

        test(pari.polcyclo(10), pari.polcyclo(5), l);

        l = ['[Mod(1, 2), Mod(0, 2); Mod(1, 2), Mod(0, 2)]',
             '[Mod(0, 3), Mod(0, 3); Mod(2, 3), Mod(2, 3)]',
             '[Mod(4294967286, 4294967295), Mod(6, 4294967295); Mod(4294967276, 4294967295), Mod(14, 4294967295)]',
             '[Mod(18446744073709551606, 18446744073709551615), Mod(6, 18446744073709551615); Mod(1844674407370955' +
             '1596, 18446744073709551615), Mod(14, 18446744073709551615)]',
             '[Mod(99999999999999999991, 100000000000000000000), Mod(6, 100000000000000000000); Mod(99999999999999' +
             '999981, 100000000000000000000), Mod(14, 100000000000000000000)]',
             '[Mod(1, 2), Mod(0, 2); Mod(1, 2), Mod(0, 2)]',
             '[Mod(1, 3), Mod(1, 3); Mod(0, 3), Mod(1, 3)]',
             '[Mod(7, 4294967295), Mod(10, 4294967295); Mod(15, 4294967295), Mod(22, 4294967295)]',
             '[Mod(7, 18446744073709551615), Mod(10, 18446744073709551615); Mod(15, 18446744073709551615), Mod(22,' +
             ' 18446744073709551615)]',
             '[Mod(7, 100000000000000000000), Mod(10, 100000000000000000000); Mod(15, 100000000000000000000), Mod(' +
             '22, 100000000000000000000)]']

        test('[1,2;3,4]', '[-1,2;-4,2]', l);
        self.assertEquals(pari.Mod(pari.Mod(1, 'y'), 'x'), 'Mod(Mod(1, y), x)')
        self.assertEquals(pari.Mod(pari.Mod(1, 'x'), 'y'), 'Mod(Mod(1, y), x)')
        with self.assertRaises(PariError) as context:
            pari.Mod(1, '"a"')
        self.assertTrue('forbidden division t_INT % t_STR' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.Mod(0, 0)
        self.assertTrue('impossible inverse in %: 0' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.Mod(0, pari.Pol(0))
        self.assertTrue('impossible inverse in %: 0' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.Mod('x+O(x^2)', 'x^3')
        self.assertTrue('inconsistent division t_SER % t_POL' in str(context.exception))
        self.assertEqual(pari.Mod('x+O(x^2)', 'x^2'), 'Mod(x, x^2)')
        self.assertEqual(pari.Mod('x+O(x^3)', 'x^2'), 'Mod(x, x^2)')
        self.assertEqual(pari.Mod(pari.Mod('x', 'x^3'), 'x^2'), 'Mod(x, x^2)')
        self.assertEqual(pari.Mod(pari.Mod(1, 12), 9), 'Mod(1, 3)')
        self.assertEqual(pari.Mod('1/x', 'x^2+1'), 'Mod(-x, x^2 + 1)')
        self.assertEqual(pari.Mod([5, 6], 2), '[Mod(1, 2), Mod(0, 2)]')
        self.assertEqual(pari.Mod('3*x', 2), 'Mod(1, 2)*x')
        self.assertEqual(pari.Mod('x', 'y'), 'Mod(1, y)*x')
        self.assertEqual(pari.Mod(pari.Pol(0), 2), 'Mod(0, 2)')
        self.assertEqual(pari.Pol(0) * pari.Mod(1, 2), 'Mod(0, 2)')
        # k = 100000000000000000000;
        # self.assertEqual(int(pow(pari.Mod(3, 7), -k)), 'Mod(2, 7)')
        # self.assertEqual(int(pow(pari.Mod(3,7)^k))
        #
        # \g1
        # a = pari.Mod(1, 2);
        # b = pari.Mod(1, 3);
        # a+b
        # a-b
        # a*b
        # a/b
        # a+a
        # a-a
        # a*a
        # a/a
        a = pari.Mod(1, 'x');
        b = pari.Mod(1, 'x+1');
        # a+b
        # a-b
        # a*b
        # a/b
        self.assertEquals(a+a, 'Mod(2, x)')
        self.assertEquals(a-a, 'Mod(0, x)')
        self.assertEquals(a*a, 'Mod(1, x)')
        self.assertEquals(a/a, 'Mod(1, x)')
        #
        #1652
        # self.assertEquals(pari.lift('Mod(271,436^56-35)^((436^56-35-1)/2)'), 'Mod(1, x)')
        #1717
        # self.assertEqual(pari.Mod(0,1), '0')
        # self.assertEqual(pari.Mod(0,1), '1')
        # self.assertEqual(pari.Mod(0,1), '-1')
        # self.assertEqual(pari.Mod(0,'x^0'), '0')
        # self.assertEqual(pari.Mod(0,'x^0'), '1')
        # self.assertEqual(pari.Mod(0,'x^0'), '-1')

"""**** Original expected results ****

1: Mod(1, 2)*x^8 + Mod(1, 2)*x^6 + Mod(1, 2)*x^4 + Mod(1, 2)*x^2 + Mod(1, 2)
2: Mod(1, 3)*x^8 + Mod(1, 3)*x^6 + Mod(1, 3)*x^4 + Mod(1, 3)*x^2 + Mod(1, 3)
3: Mod(1, 4294967295)*x^8 + Mod(1, 4294967295)*x^6 + Mod(1, 4294967295)*x^4 
+ Mod(1, 4294967295)*x^2 + Mod(1, 4294967295)
4: Mod(1, 18446744073709551615)*x^8 + Mod(1, 18446744073709551615)*x^6 + Mod
(1, 18446744073709551615)*x^4 + Mod(1, 18446744073709551615)*x^2 + Mod(1, 18
446744073709551615)
5: Mod(1, 100000000000000000000)*x^8 + Mod(1, 100000000000000000000)*x^6 + M
od(1, 100000000000000000000)*x^4 + Mod(1, 100000000000000000000)*x^2 + Mod(1
, 100000000000000000000)
1: Mod(1, 2)*x^8 + Mod(1, 2)*x^6 + Mod(1, 2)*x^4 + Mod(1, 2)*x^2 + Mod(1, 2)
2: Mod(1, 3)*x^8 + Mod(1, 3)*x^7 + Mod(2, 3)*x^5 + Mod(2, 3)*x^4 + Mod(2, 3)
*x^3 + Mod(1, 3)*x + Mod(1, 3)
3: Mod(1, 4294967295)*x^8 + Mod(4294967293, 4294967295)*x^7 + Mod(3, 4294967
295)*x^6 + Mod(4294967291, 4294967295)*x^5 + Mod(5, 4294967295)*x^4 + Mod(42
94967291, 4294967295)*x^3 + Mod(3, 4294967295)*x^2 + Mod(4294967293, 4294967
295)*x + Mod(1, 4294967295)
4: Mod(1, 18446744073709551615)*x^8 + Mod(18446744073709551613, 184467440737
09551615)*x^7 + Mod(3, 18446744073709551615)*x^6 + Mod(18446744073709551611,
 18446744073709551615)*x^5 + Mod(5, 18446744073709551615)*x^4 + Mod(18446744
073709551611, 18446744073709551615)*x^3 + Mod(3, 18446744073709551615)*x^2 +
 Mod(18446744073709551613, 18446744073709551615)*x + Mod(1, 1844674407370955
1615)
5: Mod(1, 100000000000000000000)*x^8 + Mod(99999999999999999998, 10000000000
0000000000)*x^7 + Mod(3, 100000000000000000000)*x^6 + Mod(999999999999999999
96, 100000000000000000000)*x^5 + Mod(5, 100000000000000000000)*x^4 + Mod(999
99999999999999996, 100000000000000000000)*x^3 + Mod(3, 100000000000000000000
)*x^2 + Mod(99999999999999999998, 100000000000000000000)*x + Mod(1, 10000000
0000000000000)
1: [Mod(1, 2), Mod(0, 2); Mod(1, 2), Mod(0, 2)]
2: [Mod(0, 3), Mod(0, 3); Mod(2, 3), Mod(2, 3)]
3: [Mod(4294967286, 4294967295), Mod(6, 4294967295); Mod(4294967276, 4294967
295), Mod(14, 4294967295)]
4: [Mod(18446744073709551606, 18446744073709551615), Mod(6, 1844674407370955
1615); Mod(18446744073709551596, 18446744073709551615), Mod(14, 184467440737
09551615)]
5: [Mod(99999999999999999991, 100000000000000000000), Mod(6, 100000000000000
000000); Mod(99999999999999999981, 100000000000000000000), Mod(14, 100000000
000000000000)]
1: [Mod(1, 2), Mod(0, 2); Mod(1, 2), Mod(0, 2)]
2: [Mod(1, 3), Mod(1, 3); Mod(0, 3), Mod(1, 3)]
3: [Mod(7, 4294967295), Mod(10, 4294967295); Mod(15, 4294967295), Mod(22, 42
94967295)]
4: [Mod(7, 18446744073709551615), Mod(10, 18446744073709551615); Mod(15, 184
46744073709551615), Mod(22, 18446744073709551615)]
5: [Mod(7, 100000000000000000000), Mod(10, 100000000000000000000); Mod(15, 1
00000000000000000000), Mod(22, 100000000000000000000)]
Mod(Mod(1, y), x)
Mod(Mod(1, y), x)
error("forbidden division t_INT % t_STR.")
error("impossible inverse in %: 0.")
error("impossible inverse in %: 0.")
error("inconsistent division t_SER % t_POL.")
Mod(x, x^2)
Mod(x, x^2)
Mod(x, x^2)
Mod(1, 3)
Mod(-x, x^2 + 1)
[Mod(1, 2), Mod(0, 2)]
Mod(1, 2)*x
Mod(1, y)*x
Mod(0, 2)
Mod(0, 2)
  *** _^_: Warning: Mod(a,b)^n with n >> b : wasteful.
Mod(2, 7)
  *** _^_: Warning: Mod(a,b)^n with n >> b : wasteful.
Mod(4, 7)
   debug = 1
  *** _+_: Warning: coercing quotient rings; moduli 2 and 3 -> 1.
Mod(0, 1)
  *** _-_: Warning: coercing quotient rings; moduli 2 and 3 -> 1.
Mod(0, 1)
  *** _*_: Warning: coercing quotient rings; moduli 2 and 3 -> 1.
Mod(0, 1)
  *** _/_: Warning: coercing quotient rings; moduli 2 and 3 -> 1.
Mod(0, 1)
Mod(0, 2)
Mod(0, 2)
Mod(1, 2)
Mod(1, 2)
  *** _+_: Warning: coercing quotient rings; moduli x and x + 1 -> 1.
Mod(0, 1)
  *** _-_: Warning: coercing quotient rings; moduli x and x + 1 -> 1.
Mod(0, 1)
  *** _*_: Warning: coercing quotient rings; moduli x and x + 1 -> 1.
Mod(0, 1)
  *** _/_: Warning: coercing quotient rings; moduli x and x + 1 -> 1.
Mod(0, 1)
Mod(2, x)
Mod(0, x)
Mod(1, x)
Mod(1, x)
1
1
1
1
1
1
1

"""
