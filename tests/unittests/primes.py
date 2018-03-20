# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file primes :
primes(50)
primes([-5,5])
primes([10,20])
primes([2^32-100,2^32+100])
primes([2^64-100,2^64+100])
#primes([2^50,2^50+200000])
#primes([10^7, 10^7+10^6])
#primes([2^1023+5000, 2^1023+7000])
\\#1668
primes([1,Pol(2)]);
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestPrimes(unittest.TestCase):
    def test_primes(self):
        self.assertEquals(pari.primes(50),
                          '[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,' +
                          ' 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,' +
                          ' 181, 191, 193, 197, 199, 211, 223, 227, 229]')
        self.assertEquals(pari.primes([-5, 5]), '[2, 3, 5]')
        self.assertEquals(pari.primes([10, 20]), '[11, 13, 17, 19]')
        self.assertEquals(pari.primes([pow(2, 32) - 100, pow(2, 32) + 100]),
                          '[4294967197, 4294967231, 4294967279, 4294967291, 4294967311, 4294967357, 4294967371, 429' +
                          '4967377, 4294967387, 4294967389]')
        self.assertEquals(pari.primes(['2^64-100', '2^64+100']),
                          '[18446744073709551521, 18446744073709551533, 18446744073709551557, 18446744073709551629,' +
                          ' 18446744073709551653, 18446744073709551667, 18446744073709551697, 18446744073709551709]')
        self.assertEquals(len(pari.primes([pow(2, 50), pow(2, 50) + 200000])), 5758)
        self.assertEquals(len(pari.primes([pow(10, 7), pow(10, 7) + pow(10, 6)])), 61938)
        self.assertEquals(len(pari.primes(['2^1023+5000', '2^1023+7000'])), 2)
        with self.assertRaises(PariError) as context:
            pari.primes([1, pari.Pol(2)])
        self.assertTrue('incorrect type in primes_interval (t_POL)' in str(context.exception))


"""**** Original expected results ****

[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229]
[2, 3, 5]
[11, 13, 17, 19]
[4294967197, 4294967231, 4294967279, 4294967291, 4294967311, 4294967357, 429
4967371, 4294967377, 4294967387, 4294967389]
[18446744073709551521, 18446744073709551533, 18446744073709551557, 184467440
73709551629, 18446744073709551653, 18446744073709551667, 1844674407370955169
7, 18446744073709551709]
5758
61938
2
  ***   at top-level: primes([1,Pol(2)])
  ***                 ^------------------
  *** primes: incorrect type in primes_interval (t_POL).

"""
