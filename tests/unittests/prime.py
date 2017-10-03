# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file prime :
test(N)=
{
  default(primelimit, N);
  for (b=10, 20, print1(prime(2^b), " "));
  for (b=10, 26, print1(primepi(2^b), " "));
}

test(10^6);
test(10^8);
primepi(2^32)
precprime(1)
primepi(2750160) \\ #1855
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestPrime(unittest.TestCase):
    def test_prime(self):
        def test(N, res_prime, res_primepi):
            pari.default('primelimit', N);
            for b in range(10, 21):
                self.assertEquals(pari.prime(pow(2, b)), res_prime[b - 10])
            for b in range(10, 27):
                self.assertEquals(pari.primepi(pow(2, b)), res_primepi[b - 10])

        res = ['8161', '17863', '38873', '84017', '180503', '386093',
               '821641', '1742537', '3681131', '7754077', '16290047']
        res_pi=['172', '309', '564', '1028', '1900', '3512', '6542',
                '12251', '23000', '43390', '82025', '155611', '295947',
                '564163', '1077871', '2063689', '3957809']

        test(int(pow(10, 6)), res, res_pi);
        test(int(pow(10, 8)), res, res_pi);
        self.assertEquals(pari.primepi(pow(2, 32)), '203280221')
        self.assertEquals(pari.precprime(1), '0')
        self.assertEquals(pari.primepi(2750160), '200000')  # #1855

"""**** Original expected results ****

8161 17863 38873 84017 180503 386093 821641 1742537 3681131 7754077 16290047
 172 309 564 1028 1900 3512 6542 12251 23000 43390 82025 155611 295947 56416
3 1077871 2063689 3957809 
8161 17863 38873 84017 180503 386093 821641 1742537 3681131 7754077 16290047
 172 309 564 1028 1900 3512 6542 12251 23000 43390 82025 155611 295947 56416
3 1077871 2063689 3957809 
203280221
0
200000

"""
