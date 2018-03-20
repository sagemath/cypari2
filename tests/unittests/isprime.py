# -*- coding: utf-8 -*-

"""Original pari/GP test file isprime :
isprime(5368962301599408606279497323618896374219)
isprime(4309513411435775833571)
isprime(26959946667150639794667015087019630673557916260026308143510066298881)

p=10^6+3; q=10^6+33;
isprime(1+24*p*q, 1)
isprime(1+232*p^2*q^3, 1)

isprime([2,3,4])
isprime([2,3,4],1)
isprime([2,3,4],2)
ispseudoprime([1,3,4,5],2)
\\isprime(2^3515+159, 2) 10 min
\\isprime(2^2000+841, 2) 1 min
\\isprime(2^1600+895, 2) 27s
isprime(2^1000+297, 2)

isprime(2^256+5721)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestIsprime(unittest.TestCase):
    def test_isprime(self):
        self.assertEquals(pari.isprime(5368962301599408606279497323618896374219), '1')
        self.assertEquals(pari.isprime(4309513411435775833571), '1')
        self.assertEquals(pari.isprime(26959946667150639794667015087019630673557916260026308143510066298881), '1')

        p = 10 ** 6 + 3;
        q = 10 ** 6 + 33;
        self.assertEquals(pari.isprime(1 + 24 * p * q, 1), '[2, 5, 1; 3, 2, 1; 1000003, 2, 1]')
        x = pari.isprime(1 + 232 * p ** 2 * q ** 3, 1)
        self.assertEquals(x, '[2, 3, 1; 29, 2, 1; 1000003, 2, 1]')

        self.assertEquals(pari.isprime([2, 3, 4]), '[1, 1, 0]')
        self.assertEquals(pari.isprime([2, 3, 4], 1), '[1, Mat([2, 2, 1]), 0]')
        self.assertEquals(pari.isprime([2, 3, 4], 2), '[1, 1, 0]')
        self.assertEquals(pari.ispseudoprime([1, 3, 4, 5], 2), '[0, 1, 0, 1]')
        # pari.isprime(2^3515+159, 2) 10 min
        # pari.isprime(2^2000+841, 2) 1 min
        # pari.isprime(2^1600+895, 2) 27s
        self.assertEquals(pari.isprime(2 ** 1000 + 297, 2), '1')

        self.assertEquals(pari.isprime(2 ** 256 + 5721), '1')

"""**** Original expected results ****

1
1
1

[      2 5 1]

[      3 2 1]

[1000003 2 1]


[      2 3 1]

[     29 2 1]

[1000003 2 1]

[1, 1, 0]
[1, Mat([2, 2, 1]), 0]
[1, 1, 0]
[0, 1, 0, 1]
1
1

"""
