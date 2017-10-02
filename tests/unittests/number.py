# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file number :
HEAP=[92, if(precision(1.)==38,2736,2776)];
default(realprecision,154); Pi; default(realprecision,38);
\e
addprimes([nextprime(10^9),nextprime(10^10)])
bestappr(Pi,10000)
gcdext(123456789,987654321)
bigomega(12345678987654321)
binomial(1.1,5)
chinese(Mod(7,15),Mod(13,21))
content([123,456,789,234])
contfrac(Pi)
contfrac(Pi,5)
contfrac((exp(1)-1)/(exp(1)+1),[1,3,5,7,9])
contfracpnqn([2,6,10,14,18,22,26])
contfracpnqn([1,1,1,1,1,1,1,1;1,1,1,1,1,1,1,1])
core(54713282649239)
core(54713282649239,1)
coredisc(54713282649239)
coredisc(54713282649239,1)
divisors(8!)
eulerphi(257^2)
factor(17!+1)
factor(100!+1,0)
factor(40!+1,100000)
factorback(factor(12354545545))
factor(230873846780665851254064061325864374115500032^6)
factorcantor(x^11+1,7)
centerlift(lift(factorff(x^3+x^2+x-1,3,t^3+t^2+t-1)))
10!
factorial(10)
factormod(x^11+1,7)
factormod(x^11+1,7,1)
setrand(1);ffinit(2,11)
setrand(1);ffinit(7,4)
fibonacci(100)
gcd(12345678,87654321)
gcd(x^10-1,x^15-1)
hilbert(2/3,3/4,5)
hilbert(Mod(5,7),Mod(6,7))
isfundamental(12345)
isprime(12345678901234567)
ispseudoprime(73!+1)
issquare(12345678987654321)
issquarefree(123456789876543219)
kronecker(5,7)
kronecker(3,18)
lcm(15,-21)
lift(chinese(Mod(7,15),Mod(4,21)))
modreverse(Mod(x^2+1,x^3-x-1))
moebius(3*5*7*11*13)
nextprime(100000000000000000000000)
numdiv(2^99*3^49)
omega(100!)
precprime(100000000000000000000000)
prime(100)
primes(100)
qfbclassno(-12391)
qfbclassno(1345)
qfbclassno(-12391,1)
qfbclassno(1345,1)
Qfb(2,1,3)*Qfb(2,1,3)
qfbcompraw(Qfb(5,3,-1,0.),Qfb(7,1,-1,0.))
qfbhclassno(2000003)
qfbnucomp(Qfb(2,1,9),Qfb(4,3,5),3)
form=Qfb(2,1,9);qfbnucomp(form,form,3)
qfbnupow(form,111)
qfbpowraw(Qfb(5,3,-1,0.),3)
qfbprimeform(-44,3)
qfbred(Qfb(3,10,12),,-1)
qfbred(Qfb(3,10,-20,1.5))
qfbred(Qfb(3,10,-20,1.5),2,,18)
qfbred(Qfb(3,10,-20,1.5),1)
qfbred(Qfb(3,10,-20,1.5),3,,18)
quaddisc(-252)
quadgen(-11)
quadpoly(-11)
quadregulator(17)
quadunit(17)
sigma(100)
sigma(100,2)
sigma(100,-3)
sqrtint(10!^2+1)
znorder(Mod(33,2^16+1))
forprime(p=2,100,print(p," ",lift(znprimroot(p))))
znstar(3120)
if (getheap()!=HEAP, getheap())
"""
import unittest
from cypari2 import Pari, PariError
from math import pow, factorial
from testutils import primes

pari = Pari()


class TestNumber(unittest.TestCase):
    def setUp(self):
        pari.set_real_precision(38)

    def tearDown(self):
        pari.set_real_precision(15)

    def test_number(self):
        self.assertEqual(str(pari.addprimes([pari.nextprime(1e9), pari.nextprime(1e10)])), '[1000000007, 10000000019]')
        self.assertEqual(str(pari.bestappr('Pi', 10000)), '355/113')
        self.assertEqual(str(pari.gcdext(123456789, 987654321)), '[-8, 1, 9]')
        self.assertEqual(str(pari.bigomega(12345678987654321)), '8')
        self.assertEqual(str(pari.binomial('1.1', 5)), '-0.0045457500000000000000000000000000000001')
        self.assertEqual(str(pari.chinese(pari.Mod(7, 15), pari.Mod(13, 21))), 'Mod(97, 105)')
        self.assertEqual(str(pari.content([123, 456, 789, 234])), '3')
        self.assertEqual(str(pari.divisors(factorial(8))),
                         '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 32, 35, 36, 40, ' +
                         '42, 45, 48, 56, 60, 63, 64, 70, 72, 80, 84, 90, 96, 105, 112, 120, 126, 128, 140, 144, 1' +
                         '60, 168, 180, 192, 210, 224, 240, 252, 280, 288, 315, 320, 336, 360, 384, 420, 448, 480,' +
                         ' 504, 560, 576, 630, 640, 672, 720, 840, 896, 960, 1008, 1120, 1152, 1260, 1344, 1440, 1' +
                         '680, 1920, 2016, 2240, 2520, 2688, 2880, 3360, 4032, 4480, 5040, 5760, 6720, 8064, 10080' +
                         ', 13440, 20160, 40320]')
        self.assertEqual(str(pari.eulerphi(int(pow(257, 2)))), '65792')
        self.assertEqual(str(pari.fibonacci(100)), '354224848179261915075')
        self.assertEqual(str(pari.lcm(15, -21)), '105')
        self.assertEqual(str(pari.lift(pari.chinese(pari.Mod(7, 15), pari.Mod(4, 21)))), '67')
        self.assertEqual(str(pari.modreverse(pari.Mod('x^2+1', 'x^3-x-1'))),
                         'Mod(x^2 - 3*x + 2, x^3 - 5*x^2 + 8*x - 5)')
        self.assertEqual(str(pari.moebius(3 * 5 * 7 * 11 * 13)), '-1')
        self.assertEqual(str(pari.numdiv('2^99*3^49')), '5000')
        self.assertEqual(str(pari.omega(factorial(100))), '25')
        self.assertEqual(str(pari.sqrtint('10!^2+1')), '3628800')
        self.assertEqual(str(pari.znorder(pari.Mod(33, '2^16+1'))), '2048')
        res = ['1', '2', '2', '3', '2', '2', '3', '2', '5', '2', '3', '2', '6', '3', '5', '2',
               '2', '2', '2', '7', '5', '3', '2', '3', '5']
        i = 0
        for p in primes(100):
            self.assertEquals(pari.lift(pari.znprimroot(p)), res[i])
            i += 1
        self.assertEqual(str(pari.znstar(3120)), '[768, [12, 4, 4, 2, 2], [Mod(2641, 3120), Mod(2497,' +
                         ' 3120), Mod(2341, 3120), Mod(1951, 3120), Mod(2081, 3120)]]')

    def test_primes(self):
        self.assertEqual(str(pari.nextprime(100000000000000000000000)), '100000000000000000000117')
        self.assertEqual(str(pari.precprime(100000000000000000000000)), '99999999999999999999977')
        self.assertEqual(str(pari.prime(100)), '541')
        self.assertEqual(str(pari.primes(100)),
                         '[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,' +
                         ' 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,' +
                         ' 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 27' +
                         '7, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, ' +
                         '389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491' +
                         ', 499, 503, 509, 521, 523, 541]')

    def test_contfrac(self):
        self.assertEqual(str(pari.contfrac('Pi')), '[3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2' +
                         ', 2, 2, 1, 84, 2, 1, 1, 15, 3, 13, 1, 4, 2, 6, 6]')
        self.assertEqual(str(pari.contfrac('Pi', 5)), '[3, 7, 15, 1, 292]')
        self.assertEqual(str(pari.contfrac((pari.exp(1) - 1) / (pari.exp(1) + 1), [1, 3, 5, 7, 9])),
                         '[0, 6, 10, 42, 30]')

    def test_contfracpnqn(self):
        self.assertEqual(str(pari.contfracpnqn([2, 6, 10, 14, 18, 22, 26])), '[19318376, 741721; 8927353, 342762]')
        self.assertEqual(str(pari.contfracpnqn('[1,1,1,1,1,1,1,1;1,1,1,1,1,1,1,1]')), '[34, 21; 21, 13]')

    def test_core(self):
        self.assertEqual(str(pari.core(54713282649239)), '5471')
        self.assertEqual(str(pari.core(54713282649239, 1)), '[5471, 100003]')

    def test_coredisc(self):
        self.assertEqual(str(pari.coredisc(54713282649239)), '21884')
        self.assertEqual(str(pari.coredisc(54713282649239, 1)), '[21884, 100003/2]')

    def test_factor(self):
        self.assertEqual(str(pari.factor(factorial(17) + 1)), '[661, 1; 537913, 1; 1000357, 1]')
        self.assertEqual(str(pari.factor(factorial(100) + 1, 0)),
                         '[101, 1; 14303, 1; 149239, 1; 4328852738498929626130718009186589490596793086850244817957' +
                         '4076552756849301072702375746139749880098152144087781328865783919562249722562149942762845' +
                         '3, 1]')
        self.assertEqual(str(pari.factor(factorial(40) + 1, 100000)),
                         '[41, 1; 59, 1; 277, 1; 1217669507565553887239873369513188900554127, 1]')
        self.assertEqual(str(pari.factorback(pari.factor(12354545545))), '12354545545')
        self.assertEqual(str(pari.factor('230873846780665851254064061325864374115500032^6')),
                         '[2, 120; 3, 6; 7, 6; 23, 6; 29, 6; 500501, 36]')
        self.assertEqual(str(pari.factorcantor('x^11+1', 7)), '[Mod(1, 7)*x + Mod(1, 7), 1; Mod(1, 7)*x^10 + ' +
                         'Mod(6, 7)*x^9 + Mod(1, 7)*x^8 + Mod(6, 7)*x^7 + Mod(1, 7)*x^6 + Mod(6, 7)*x^5 + Mo' +
                         'd(1, 7)*x^4 + Mod(6, 7)*x^3 + Mod(1, 7)*x^2 + Mod(6, 7)*x + Mod(1, 7), 1]')
        self.assertEqual(str(pari.centerlift(pari.lift(pari.factorff('x^3+x^2+x-1', 3, 't^3+t^2+t-1')))),
                         '[x - t, 1; x + (t^2 + t - 1), 1; x + (-t^2 - 1), 1]')
        self.assertEqual(str(pari('10!')), '3628800')
        self.assertEqual(str(pari.factorial(10)), '3628800.0000000000000000000000000000000')

    def test_factormod(self):
        self.assertEqual(str(pari.factormod('x^11+1', 7)),
                         '[Mod(1, 7)*x + Mod(1, 7), 1; Mod(1, 7)*x^10 + Mod(6, 7)*x^9 + Mod(1, 7)*x^8 + Mod(6, 7)*' +
                         'x^7 + Mod(1, 7)*x^6 + Mod(6, 7)*x^5 + Mod(1, 7)*x^4 + Mod(6, 7)*x^3 + Mod(1, 7)*x^2 + Mo' +
                         'd(6, 7)*x + Mod(1, 7), 1]')
        self.assertEqual(str(pari.factormod('x^11+1', 7, 1)), '[1, 1; 10, 1]')

    def test_ffinit(self):
        pari.setrand(1);
        self.assertEqual(str(pari.ffinit(2, 11)),
                         'Mod(1, 2)*x^11 + Mod(1, 2)*x^10 + Mod(1, 2)*x^8 + Mod(1, 2)*x^4 + Mod(1, 2)*x^3' +
                         ' + Mod(1, 2)*x^2 + Mod(1, 2)')
        pari.setrand(1);
        self.assertEqual(str(pari.ffinit(7, 4)),
                         'Mod(1, 7)*x^4 + Mod(1, 7)*x^3 + Mod(1, 7)*x^2 + Mod(1, 7)*x + Mod(1, 7)')

    def test_gcd(self):
        self.assertEqual(str(pari.gcd(12345678, 87654321)), '9')
        self.assertEqual(str(pari.gcd('x^10-1', 'x^15-1')), 'x^5 - 1')

    def test_hilbert(self):
        self.assertEqual(str(pari.hilbert('2/3', '3/4', 5)), '1')
        self.assertEqual(str(pari.hilbert(pari.Mod(5, 7), pari.Mod(6, 7))), '1')

    def test_booleanfct(self):
        self.assertTrue(pari.isfundamental(12345))
        self.assertFalse(pari.isprime(12345678901234567))
        self.assertTrue(pari.ispseudoprime(factorial(73) + 1))
        self.assertTrue(pari(12345678987654321).issquare())
        self.assertFalse(pari.issquarefree(123456789876543219))

    def test_kronecker(self):
        self.assertEqual(str(pari.kronecker(5, 7)), '-1')
        self.assertEqual(str(pari.kronecker(3, 18)), '0')

    def test_qfbclassno(self):
        self.assertEqual(str(pari.qfbclassno(-12391)), '63')
        self.assertEqual(str(pari.qfbclassno(1345)), '6')
        self.assertEqual(str(pari.qfbclassno(-12391, 1)), '63')
        self.assertEqual(str(pari.qfbclassno(1345, 1)), '6')

    def test_qfb(self):
        self.assertEqual(str(pari.Qfb(2, 1, 3) * pari.Qfb(2, 1, 3)), 'Qfb(2, -1, 3)')
        self.assertEqual(str(pari.qfbcompraw(pari.Qfb(5, 3, -1, '0.'), pari.Qfb(7, 1, -1, '0.'))),
                         'Qfb(35, 43, 13, 0.E-38)')
        self.assertEqual(str(pari.qfbhclassno(2000003)), '357')
        self.assertEqual(str(pari.qfbnucomp(pari.Qfb(2, 1, 9), pari.Qfb(4, 3, 5), 3)), 'Qfb(2, -1, 9)')
        form = pari.Qfb(2, 1, 9);
        self.assertEqual(str(pari.qfbnucomp(form, form, 3)), 'Qfb(4, -3, 5)')
        self.assertEqual(str(pari.qfbnupow(form, 111)), 'Qfb(2, -1, 9)')
        self.assertEqual(str(pari.qfbpowraw(pari.Qfb(5, 3, -1, '0.'), 3)), 'Qfb(125, 23, 1, 0.E-38)')
        self.assertEqual(str(pari.qfbprimeform(-44, 3)), 'Qfb(3, 2, 4)')

    def test_qfbred(self):
        self.assertEqual(str(pari.qfbred(pari.Qfb(3, 10, 12), 0, -1)), 'Qfb(3, -2, 4)')
        self.assertEqual(str(pari.qfbred(pari.Qfb(3, 10, -20, 1.5, precision=127))),
                         'Qfb(3, 16, -7, 1.5000000000000000000000000000000000000)')
        self.assertEqual(str(pari.qfbred(pari.Qfb(3, 10, -20, 1.5, precision=127), 2, None, 18)),
                         'Qfb(3, 16, -7, 1.5000000000000000000000000000000000000)')
        self.assertEqual(str(pari.qfbred(pari.Qfb(3, 10, -20, 1.5, precision=127), 1)),
                         'Qfb(-20, -10, 3, 2.1074451073987839947135880252731470616)')
        self.assertEqual(str(pari.qfbred(pari.Qfb(3, 10, -20, 1.5, precision=127), 3, None, 18)),
                         'Qfb(-20, -10, 3, 1.5000000000000000000000000000000000000)')

    def test_quadfct(self):
        self.assertEqual(str(pari.quaddisc(-252)), '-7')
        self.assertEqual(str(pari.quadgen(-11)), 'w')
        self.assertEqual(str(pari.quadpoly(-11)), 'x^2 - x + 3')
        self.assertEqual(str(pari.quadregulator(17, precision=127)), '2.0947125472611012942448228460655286535')
        self.assertEqual(str(pari.quadunit(17)), '3 + 2*w')

    def test_sigma(self):
        self.assertEqual(str(pari.sigma(100)), '217')
        self.assertEqual(str(pari.sigma(100, 2)), '13671')
        self.assertEqual(str(pari.sigma(100, -3)), '1149823/1000000')

"""**** Original expected results ****

   echo = 1 (on)
? addprimes([nextprime(10^9),nextprime(10^10)])
[1000000007, 10000000019]
? bestappr(Pi,10000)
355/113
? gcdext(123456789,987654321)
[-8, 1, 9]
? bigomega(12345678987654321)
8
? binomial(1.1,5)
-0.0045457500000000000000000000000000000001
? chinese(Mod(7,15),Mod(13,21))
Mod(97, 105)
? content([123,456,789,234])
3
? contfrac(Pi)
[3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2, 2, 2, 1, 84, 2, 1
, 1, 15, 3, 13, 1, 4, 2, 6, 6]
? contfrac(Pi,5)
[3, 7, 15, 1, 292]
? contfrac((exp(1)-1)/(exp(1)+1),[1,3,5,7,9])
[0, 6, 10, 42, 30]
? contfracpnqn([2,6,10,14,18,22,26])

[19318376 741721]

[ 8927353 342762]

? contfracpnqn([1,1,1,1,1,1,1,1;1,1,1,1,1,1,1,1])

[34 21]

[21 13]

? core(54713282649239)
5471
? core(54713282649239,1)
[5471, 100003]
? coredisc(54713282649239)
21884
? coredisc(54713282649239,1)
[21884, 100003/2]
? divisors(8!)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 32, 
35, 36, 40, 42, 45, 48, 56, 60, 63, 64, 70, 72, 80, 84, 90, 96, 105, 112, 12
0, 126, 128, 140, 144, 160, 168, 180, 192, 210, 224, 240, 252, 280, 288, 315
, 320, 336, 360, 384, 420, 448, 480, 504, 560, 576, 630, 640, 672, 720, 840,
 896, 960, 1008, 1120, 1152, 1260, 1344, 1440, 1680, 1920, 2016, 2240, 2520,
 2688, 2880, 3360, 4032, 4480, 5040, 5760, 6720, 8064, 10080, 13440, 20160, 
40320]
? eulerphi(257^2)
65792
? factor(17!+1)

[    661 1]

[ 537913 1]

[1000357 1]

? factor(100!+1,0)

[101 1]

[14303 1]

[149239 1]

[432885273849892962613071800918658949059679308685024481795740765527568493010
727023757461397498800981521440877813288657839195622497225621499427628453 1]

? factor(40!+1,100000)

[                                         41 1]

[                                         59 1]

[                                        277 1]

[1217669507565553887239873369513188900554127 1]

? factorback(factor(12354545545))
12354545545
? factor(230873846780665851254064061325864374115500032^6)

[     2 120]

[     3   6]

[     7   6]

[    23   6]

[    29   6]

[500501  36]

? factorcantor(x^11+1,7)

[Mod(1, 7)*x + Mod(1, 7) 1]

[Mod(1, 7)*x^10 + Mod(6, 7)*x^9 + Mod(1, 7)*x^8 + Mod(6, 7)*x^7 + Mod(1, 7)*
x^6 + Mod(6, 7)*x^5 + Mod(1, 7)*x^4 + Mod(6, 7)*x^3 + Mod(1, 7)*x^2 + Mod(6,
 7)*x + Mod(1, 7) 1]

? centerlift(lift(factorff(x^3+x^2+x-1,3,t^3+t^2+t-1)))

[            x - t 1]

[x + (t^2 + t - 1) 1]

[   x + (-t^2 - 1) 1]

? 10!
3628800
? factorial(10)
3628800.0000000000000000000000000000000
? factormod(x^11+1,7)

[Mod(1, 7)*x + Mod(1, 7) 1]

[Mod(1, 7)*x^10 + Mod(6, 7)*x^9 + Mod(1, 7)*x^8 + Mod(6, 7)*x^7 + Mod(1, 7)*
x^6 + Mod(6, 7)*x^5 + Mod(1, 7)*x^4 + Mod(6, 7)*x^3 + Mod(1, 7)*x^2 + Mod(6,
 7)*x + Mod(1, 7) 1]

? factormod(x^11+1,7,1)

[ 1 1]

[10 1]

? setrand(1);ffinit(2,11)
Mod(1, 2)*x^11 + Mod(1, 2)*x^10 + Mod(1, 2)*x^8 + Mod(1, 2)*x^4 + Mod(1, 2)*
x^3 + Mod(1, 2)*x^2 + Mod(1, 2)
? setrand(1);ffinit(7,4)
Mod(1, 7)*x^4 + Mod(1, 7)*x^3 + Mod(1, 7)*x^2 + Mod(1, 7)*x + Mod(1, 7)
? fibonacci(100)
354224848179261915075
? gcd(12345678,87654321)
9
? gcd(x^10-1,x^15-1)
x^5 - 1
? hilbert(2/3,3/4,5)
1
? hilbert(Mod(5,7),Mod(6,7))
1
? isfundamental(12345)
1
? isprime(12345678901234567)
0
? ispseudoprime(73!+1)
1
? issquare(12345678987654321)
1
? issquarefree(123456789876543219)
0
? kronecker(5,7)
-1
? kronecker(3,18)
0
? lcm(15,-21)
105
? lift(chinese(Mod(7,15),Mod(4,21)))
67
? modreverse(Mod(x^2+1,x^3-x-1))
Mod(x^2 - 3*x + 2, x^3 - 5*x^2 + 8*x - 5)
? moebius(3*5*7*11*13)
-1
? nextprime(100000000000000000000000)
100000000000000000000117
? numdiv(2^99*3^49)
5000
? omega(100!)
25
? precprime(100000000000000000000000)
99999999999999999999977
? prime(100)
541
? primes(100)
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 2
39, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 33
1, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421
, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509,
 521, 523, 541]
? qfbclassno(-12391)
63
? qfbclassno(1345)
6
? qfbclassno(-12391,1)
63
? qfbclassno(1345,1)
6
? Qfb(2,1,3)*Qfb(2,1,3)
Qfb(2, -1, 3)
? qfbcompraw(Qfb(5,3,-1,0.),Qfb(7,1,-1,0.))
Qfb(35, 43, 13, 0.E-38)
? qfbhclassno(2000003)
357
? qfbnucomp(Qfb(2,1,9),Qfb(4,3,5),3)
Qfb(2, -1, 9)
? form=Qfb(2,1,9);qfbnucomp(form,form,3)
Qfb(4, -3, 5)
? qfbnupow(form,111)
Qfb(2, -1, 9)
? qfbpowraw(Qfb(5,3,-1,0.),3)
Qfb(125, 23, 1, 0.E-38)
? qfbprimeform(-44,3)
Qfb(3, 2, 4)
? qfbred(Qfb(3,10,12),,-1)
Qfb(3, -2, 4)
? qfbred(Qfb(3,10,-20,1.5))
Qfb(3, 16, -7, 1.5000000000000000000000000000000000000)
? qfbred(Qfb(3,10,-20,1.5),2,,18)
Qfb(3, 16, -7, 1.5000000000000000000000000000000000000)
? qfbred(Qfb(3,10,-20,1.5),1)
Qfb(-20, -10, 3, 2.1074451073987839947135880252731470616)
? qfbred(Qfb(3,10,-20,1.5),3,,18)
Qfb(-20, -10, 3, 1.5000000000000000000000000000000000000)
? quaddisc(-252)
-7
? quadgen(-11)
w
? quadpoly(-11)
x^2 - x + 3
? quadregulator(17)
2.0947125472611012942448228460655286535
? quadunit(17)
3 + 2*w
? sigma(100)
217
? sigma(100,2)
13671
? sigma(100,-3)
1149823/1000000
? sqrtint(10!^2+1)
3628800
? znorder(Mod(33,2^16+1))
2048
? forprime(p=2,100,print(p," ",lift(znprimroot(p))))
2 1
3 2
5 2
7 3
11 2
13 2
17 3
19 2
23 5
29 2
31 3
37 2
41 6
43 3
47 5
53 2
59 2
61 2
67 2
71 7
73 5
79 3
83 2
89 3
97 5
? znstar(3120)
[768, [12, 4, 4, 2, 2], [Mod(2641, 3120), Mod(2497, 3120), Mod(2341, 3120), 
Mod(1951, 3120), Mod(2081, 3120)]]
? if(getheap()!=HEAP,getheap())

"""
