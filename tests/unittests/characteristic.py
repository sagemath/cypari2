# -*- coding: utf-8 -*-

"""Original pari/GP test file characteristic :
v=[1,1.,Mod(1,6),1/2,I+Mod(1,3), O(2), quadgen(5)*Mod(1,3), Mod(1,x)];
for (i=1,#v, print(characteristic(v[i])))
characteristic(v)
characteristic(matid(2)*Mod(1,2))
characteristic([])
characteristic(List())
characteristic(ffgen(2^3))
characteristic([ffgen(2),ffgen(3)])
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestCharacteristic(unittest.TestCase):
    def test_characteristic(self):
        v = [1, '1.', pari.Mod(1, 6), '1/2', 'I' + pari.Mod(1, 3), 'O(2)', pari.quadgen(5) * pari.Mod(1, 3),
             pari.Mod(1, 'x')]
        d = ['0', '0', '6', '0', '3', '0', '3', '0']
        for i in range(0,len(v)):
            self.assertEquals(str(pari.characteristic(v[i])), d[i])
        self.assertEquals(str(pari.characteristic(v)), '3')
        self.assertEquals(str(pari.characteristic(pari.matid(2)*pari.Mod(1,2))), '2')
        self.assertEquals(str(pari.characteristic([])), '0')
        self.assertEquals(str(pari.characteristic(pari.List())), '0')
        self.assertEquals(str(pari.characteristic(pari.ffgen('2^3'))), '2')
        with self.assertRaises(PariError) as context:
            pari.characteristic([pari.ffgen(2), pari.ffgen(3)])
        self.assertTrue('inconsistent moduli in characteristic: 2 != 3' in str(context.exception))

"""**** Original expected results ****

0
0
6
0
3
0
3
0
3
2
0
0
2
  ***   at top-level: characteristic([ffge
  ***                 ^--------------------
  *** characteristic: inconsistent moduli in characteristic: 2 != 3

"""
