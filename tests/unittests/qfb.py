# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file qfb :
vec(x) = [component(x,1), component(x,2), component(x,3)];
vec( qfbred(Qfb(6,6,-1),1) )
default(realprecision,38)
q=Qfb(7, 30, -14)^2;
qfbpowraw(q,-1)
q*q^2
q^0
q^1
q^-1
q^-(2^64+1)
q=Qfb(2, 1, 3); q2=q*q;
q3=qfbcompraw(q,q2)
qfbpowraw(q,3)
qfbred(q3,1)
q=Qfb(1009, 60, 99108027750247771)
qfbnupow(q, 8839368315)
L = sqrtnint(abs(poldisc(q)), 4);
qfbnupow(q, 8839368315,L)
q=Qfb(22000957029,25035917443,7122385192);
qfbred(q)
qfbredsl2(q)
q=Qfb(1099511627776,1879224363605,802966544317);
[qr,U]=qfbredsl2(q)
qfeval(q,U)
qfeval(q,U[,1])
qfeval(q,U[,2])
qfeval(q,U[,1],U[,2])
D=poldisc(q);
qfbredsl2(q,[D,sqrtint(D)])
qfbredsl2(q,[D]);
qfbredsl2(q,[D,1.]);
p=2^64+13;
qfbprimeform(-4,p)
qfbprimeform(5,p)

"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestQfb(unittest.TestCase):
    def test_qfb(self):
        def vec(x):
            return [pari.component(x, 1), pari.component(x, 2), pari.component(x, 3)];

        self.assertEquals(str(vec(pari.qfbred(pari.Qfb(6, 6, -1), 1))), '[-1, 6, 6]')
        pari.set_real_precision(38)
        q=pari('Qfb(7, 30, -14)^2');
        self.assertEquals(pari.qfbpowraw(q,-1), 'Qfb(-2, -34, 17, -1.2031810657666797073140254201751247272)')
        # q*q^2
        # q^0
        # q^1
        # q^-1
        # q^-(2^64+1)
        q = pari.Qfb(2, 1, 3);
        q2 = pari('Qfb(2, 1, 3)*Qfb(2, 1, 3)');
        q3 = pari.qfbcompraw(q, q2)
        self.assertEquals(q3, 'Qfb(1, -1, 6)')
        self.assertEquals(pari.qfbpowraw(q, 3), 'Qfb(8, 13, 6)')
        self.assertEquals(pari.qfbred(q3, 1), 'Qfb(1, 1, 6)')
        q = pari.Qfb(1009, 60, 99108027750247771)
        self.assertEquals(q, 'Qfb(1009, 60, 99108027750247771)')
        self.assertEquals(pari.qfbnupow(q, 8839368315), 'Qfb(1, 0, 100000000000000000039)')
        L = pari.sqrtnint(pari.abs(pari.poldisc(q)), 4);
        self.assertEquals(pari.qfbnupow(q, 8839368315, L), 'Qfb(1, 0, 100000000000000000039)')
        q = pari.Qfb(22000957029, 25035917443, 7122385192);
        self.assertEquals(pari.qfbred(q), 'Qfb(1, 1, 6)')
        self.assertEquals(pari.qfbredsl2(q), '[Qfb(1, 1, 6), [22479, 76177; -39508, -133885]]')

        q = pari.Qfb('1099511627776', '1879224363605', '802966544317', precision=128);
        U = pari.qfbredsl2(q)[1]
        self.assertEquals(U, '[127327, -416128; -148995, 486943]')
        self.assertEquals(pari.qfeval(q, U), 'Qfb(4, 3, -3, 0.E-38)')
        self.assertEquals(pari.qfeval(q, 'qfbredsl2(Qfb(1099511627776,1879224363605,802966544317))[2][,1]'), '4')
        self.assertEquals(pari.qfeval(q, 'qfbredsl2(Qfb(1099511627776,1879224363605,802966544317))[2][,2]'), '-3')
        self.assertEquals(pari.qfeval(q, 'qfbredsl2(Qfb(1099511627776,1879224363605,802966544317))[2][,1]',
                                      'qfbredsl2(Qfb(1099511627776,1879224363605,802966544317))[2][,2]'), '3/2')
        D = pari.poldisc(q);
        self.assertEquals(pari.qfbredsl2(q, [D, pari.sqrtint(D)]),
                          '[Qfb(4, 3, -3, 0.E-38), [127327, -416128; -148995, 486943]]')
        with self.assertRaises(PariError) as context:
            pari.qfbredsl2(q, [D]);
        self.assertTrue('incorrect type in qfbredsl2 (t_VEC)' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.qfbredsl2(q, [D, 1.]);
        self.assertTrue('incorrect type in qfbredsl2 (t_VEC)' in str(context.exception))

        p = pow(2, 64) + 13;
        self.assertEquals(pari.qfbprimeform(-4, p),
                          'Qfb(18446744073709551629, 4741036151112220792, 304625896260305173)')
        self.assertEquals(pari.qfbprimeform(5, p),
                          'Qfb(18446744073709551629, 7562574061564804959, 775103267656920011, 0.E-38)')
        pari.set_real_precision(15)
        

"""**** Original expected results ****

[-1, 6, 6]
Qfb(-2, -34, 17, -1.2031810657666797073140254201751247272)
Qfb(-2, 34, 17, 3.6095431973000391219420762605253741816)
Qfb(1, 34, -34, 0.E-38)
Qfb(-2, 34, 17, 1.2031810657666797073140254201751247272)
Qfb(17, 34, -2, -2.9945542852277529726974917240067615601)
Qfb(17, 34, -2, -22194773194531041164.334277319893643413)
Qfb(1, -1, 6)
Qfb(8, 13, 6)
Qfb(1, 1, 6)
Qfb(1009, 60, 99108027750247771)
Qfb(1, 0, 100000000000000000039)
Qfb(1, 0, 100000000000000000039)
Qfb(1, 1, 6)
[Qfb(1, 1, 6), [22479, 76177; -39508, -133885]]
[Qfb(4, 3, -3, 0.E-38), [127327, -416128; -148995, 486943]]
Qfb(4, 3, -3, 0.E-38)
4
-3
3/2
[Qfb(4, 3, -3, 0.E-38), [127327, -416128; -148995, 486943]]
  ***   at top-level: qfbredsl2(q,[D])
  ***                 ^----------------
  *** qfbredsl2: incorrect type in qfbredsl2 (t_VEC).
  ***   at top-level: qfbredsl2(q,[D,1.])
  ***                 ^-------------------
  *** qfbredsl2: incorrect type in qfbredsl2 (t_VEC).
Qfb(18446744073709551629, 4741036151112220792, 304625896260305173)
Qfb(18446744073709551629, 7562574061564804959, 775103267656920011, 0.E-38)

"""
