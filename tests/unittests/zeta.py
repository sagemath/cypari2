# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file zeta :
default(realprecision,38);
allocatemem(20*10^6);
zeta(3+O(5^10))
zeta(1 + I/100)
zeta(1000.5)
zeta(1000)
zeta(100)
zeta(31)
zeta(100+100*I)
zeta(60+I)
zeta(-1000+I)
zeta(2+O(2^10))
zeta(2^64)
zeta(-2^64)
iferr(zeta(-1-2^64),E,E)
zeta(2+1e-101*I)
zeta(1.01)
zeta(1e-32)
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestZeta(unittest.TestCase):
    def test_zeta(self):
        pari.set_real_precision(38)
        pari.allocatemem(2e7);
        self.assertEquals(pari.zeta('3+O(5^10)'), '2*5^-1 + 2*5 + 3*5^2 + 3*5^4 + 3*5^5 + 2*5^6 + 5^7 + 4*5^8 + O(5^9)')
        self.assertEquals(pari.zeta('1 + I/100', precision=128),
                          '0.57721614942066140874800424251188396262 - 99.999271841202858157138397118797159155*I')
        self.assertEquals(pari.zeta('1000.5', precision=128), '1.0000000000000000000000000000000000000')
        self.assertEquals(pari.zeta(1000, precision=128), '1.0000000000000000000000000000000000000')
        self.assertEquals(str(pari.zeta(100, precision=128)), '1.0000000000000000000000000000007888609')
        self.assertEquals(str(pari.zeta(31, precision=128)), '1.0000000004656629065033784072989233251')
        self.assertEquals(str(pari.zeta('100+100*I', precision=128)),
                          '1.0000000000000000000000000000007731864 - 1.5647480679975229240431199238639049803 E-31*I')
        self.assertEquals(str(pari.zeta('60+I', precision=128)),
                          '1.0000000000000000006672083904260744090 - 5.5421056315169138713580539141777567374 E-19*I')
        self.assertEquals(str(pari.zeta('-1000+I', precision=128)), '-1.8236338315400224657144248914124703368 E1769 + '
                                                                    '6.8223788001755144705322033655798283436 E1768*I')
        self.assertEquals(pari.zeta('2+O(2^10)', precision=128), '2^-1 + 1 + 2^2 + 2^3 + 2^5 + 2^6 + 2^7 + O(2^9)')
        self.assertEquals(pari.zeta(pow(2, 64), precision=128), '1.0000000000000000000000000000000000000')
        self.assertEquals(pari.zeta('-2^64', precision=128), '0.E-38')

        with self.assertRaises(PariError) as context:
            pari.zeta('-1-2^64')
        self.assertTrue('overflow in zeta [large negative argument]' in str(context.exception))

        self.assertEquals(str(pari.zeta('2+1e-101*I', precision=128)),
                          '1.6449340668482264364724151666460251892 - 9.3754825431584375370257409456786497790 E-102*I')
        self.assertEquals(str(pari.zeta('1.01', precision=128)), '100.57794333849687249028215428579024415')
        self.assertEquals(str(pari.zeta('1e-32', precision=128)), '-0.50000000000000000000000000000000918939')
        pari.set_real_precision(15)

"""**** Original expected results ****

  ***   Warning: new stack size = 20000000 (19.073 Mbytes).
2*5^-1 + 2*5 + 3*5^2 + 3*5^4 + 3*5^5 + 2*5^6 + 5^7 + 4*5^8 + O(5^9)
0.57721614942066140874800424251188396262 - 99.999271841202858157138397118797
159155*I
1.0000000000000000000000000000000000000
1.0000000000000000000000000000000000000
1.0000000000000000000000000000007888609
1.0000000004656629065033784072989233251
1.0000000000000000000000000000007731864 - 1.56474806799752292404311992386390
49803 E-31*I
1.0000000000000000006672083904260744090 - 5.54210563151691387135805391417775
67374 E-19*I
-1.8236338315400224657144248914124703368 E1769 + 6.8223788001755144705322033
655798283436 E1768*I
2^-1 + 1 + 2^2 + 2^3 + 2^5 + 2^6 + 2^7 + O(2^9)
1.0000000000000000000000000000000000000
0.E-38
error("overflow in zeta [large negative argument].")
1.6449340668482264364724151666460251892 - 9.37548254315843753702574094567864
97790 E-102*I
100.57794333849687249028215428579024415
-0.50000000000000000000000000000000918939

"""
