# -*- coding: utf-8 -*-

"""Original pari/GP test file galpol :
\\ package: galpol

galoisgetpol(8)
for(i=1,5,print(galoisgetpol(8,i)))
for(i=1,5,print(galoisgetpol(8,i,2)))
galoisgetpol(8,6)
galoisgetpol(3,1,3)
galoisgetpol(3,1,2)
test(n,k)=
  if(galoisidentify(galoisinit(galoisgetpol(n,k)[1])) != [n,k], error([n,k]));
test(8,3)
test(18,5)
test(27,3)
test(45,2)
test(30,4)
test(32,4)
test(32,13)
test(32,30)
test(32,32)
test(42,2)
test(48,12)
test(64,3)
test(64,14)
test(64,16)
test(64,48)
test(64,51)
test(64,70)
test(64,68)
test(64,80)
test(64,44)
galoisidentify(galoisinit(polcyclo(390)))
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestGalpol(unittest.TestCase):
    def test_galpol(self):
        # package: galpol

        self.assertEquals(pari.galoisgetpol(8), '5')
        l = ['[x^8 - x^7 - 7*x^6 + 6*x^5 + 15*x^4 - 10*x^3 - 10*x^2 + 4*x + 1, 1]',
             '[x^8 - 7*x^6 + 14*x^4 - 8*x^2 + 1, 1]',
             '[x^8 - 4*x^7 - 8*x^6 + 24*x^5 + 30*x^4 - 16*x^3 - 20*x^2 + 2, 3]',
             '[x^8 - 12*x^6 + 36*x^4 - 36*x^2 + 9, 3]',
             '[x^8 - 12*x^6 + 23*x^4 - 12*x^2 + 1, 7]']
        for i in range(1,6):
            self.assertEquals(pari.galoisgetpol(8,i), l[i-1])
        l = ['[x^8 + 8*x^6 + 20*x^4 + 16*x^2 + 2, 1]',
             '[x^8 - x^7 + x^5 - x^4 + x^3 - x + 1, 1]',
             '[x^8 + 3*x^4 + 1, 1]',
             '[x^8 + 12*x^6 + 36*x^4 + 36*x^2 + 9, 3]',
             '[x^8 - x^4 + 1, 1]']
        for i in range(1, 6):
            self.assertEquals(pari.galoisgetpol(8, i, 2), l[i - 1])
        with self.assertRaises(PariError) as context:
            pari.galoisgetpol(8, 6)
        self.assertTrue('domain error in galoisgetpol: group index > 5' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.galoisgetpol(3, 1, 3)
        self.assertTrue('invalid flag in galoisgetpol' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.galoisgetpol(3, 1, 2)
        self.assertTrue('domain error in galoisgetpol: s > 1' in str(context.exception))
        # test(n,k)=
        #   if(pari.galoisidentify(pari.galoisinit(pari.galoisgetpol(n,k)[1])) != [n,k], error([n,k]));
        # test(8,3)
        # test(18,5)
        # test(27,3)
        # test(45,2)
        # test(30,4)
        # test(32,4)
        # test(32,13)
        # test(32,30)
        # test(32,32)
        # test(42,2)
        # test(48,12)
        # test(64,3)
        # test(64,14)
        # test(64,16)
        # test(64,48)
        # test(64,51)
        # test(64,70)
        # test(64,68)
        # test(64,80)
        # test(64,44)
        self.assertEquals(pari.galoisidentify(pari.galoisinit(pari.polcyclo(390))), '[96, 161]')

"""**** Original expected results ****

5
[x^8 - x^7 - 7*x^6 + 6*x^5 + 15*x^4 - 10*x^3 - 10*x^2 + 4*x + 1, 1]
[x^8 - 7*x^6 + 14*x^4 - 8*x^2 + 1, 1]
[x^8 - 4*x^7 - 8*x^6 + 24*x^5 + 30*x^4 - 16*x^3 - 20*x^2 + 2, 3]
[x^8 - 12*x^6 + 36*x^4 - 36*x^2 + 9, 3]
[x^8 - 12*x^6 + 23*x^4 - 12*x^2 + 1, 7]
[x^8 + 8*x^6 + 20*x^4 + 16*x^2 + 2, 1]
[x^8 - x^7 + x^5 - x^4 + x^3 - x + 1, 1]
[x^8 + 3*x^4 + 1, 1]
[x^8 + 12*x^6 + 36*x^4 + 36*x^2 + 9, 3]
[x^8 - x^4 + 1, 1]
  ***   at top-level: galoisgetpol(8,6)
  ***                 ^-----------------
  *** galoisgetpol: domain error in galoisgetpol: group index > 5
  ***   at top-level: galoisgetpol(3,1,3)
  ***                 ^-------------------
  *** galoisgetpol: invalid flag in galoisgetpol.
  ***   at top-level: galoisgetpol(3,1,2)
  ***                 ^-------------------
  *** galoisgetpol: domain error in galoisgetpol: s > 1
[96, 161]

"""
