# -*- coding: utf-8 -*-

"""Original pari/GP test file lindep :
lindep([sqrt(2), sqrt(3), sqrt(2)+sqrt(3)])
lindep([1, 2 + 3 + 3^2 + 3^3 + 3^4 + O(3^5)])
lindep([1,2,3;4,5,6;7,8,9])
lindep([x*y, x^2 + y, x^2*y + x*y^2, 1])
z = sqrt(1+5*y+y^2+y^3);
seralgdep(z, 2,3)
seralgdep(z, 2,2)
seralgdep(1/(1-y+O(y^5)), 1,1)
seralgdep(1+5*y+O(y^3), 1,10)
lindep([])
lindep([0])
lindep([1])
lindep([1,I])
algdep(1,0)
algdep(1,-1)
z=sqrt(2+O(7^4)); algdep(z,2)
lindep(Mod([E*x, E*x + E, E^2*x^2 + E*x + 2*E], E^3))
lindep([[1,0,0],[0,1,0],[1,1,0]])
lindep([[1,0,0]~,[0,1,0]~,[1,1,0]~])
lindep([[1,0,0]~,[0,1,0]~,[1,1,1]~])
lindep([[1,0,0]~,[0,1,0],[1,1,0]])
lindep([[1,0,0]~,[0,1,0]~,[1,1,0]~])

"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestLindep(unittest.TestCase):
    def setUp(self):
        pari.set_real_precision(15)
    def test_lindep(self):
        self.assertEquals(pari.lindep([pari.sqrt(2), pari.sqrt(3), pari.sqrt(2) + pari.sqrt(3)]), '[-1, -1, 1]~')
        self.assertEquals(pari.lindep('[1, 2 + 3 + 3^2 + 3^3 + 3^4 + O(3^5)]'), '[1, -2]~')
        self.assertEquals(pari.lindep('[1,2,3;4,5,6;7,8,9]'), '[1, -2, 1]~')
        self.assertEquals(pari.lindep(['x*y', 'x^2 + y', 'x^2*y + x*y^2', 1]), '[y, y, -1, -y^2]~')
        self.assertEquals(pari.lindep([]), '[]~')
        self.assertEquals(pari.lindep([0]), '[1]~')
        self.assertEquals(pari.lindep([1]), '[]~')
        self.assertEquals(pari.lindep([1, 'I']), '[]~')
        self.assertEquals(pari.lindep(pari.Mod(['E*x', 'E*x + E', 'E^2*x^2 + E*x + 2*E'], 'E^3')),
                          '[Mod(0, E^3), Mod(0, E^3), Mod(0, E^3)]~')
        self.assertEquals(pari.lindep([[1, 0, 0], [0, 1, 0], [1, 1, 0]]), '[1, 1, -1]~')
        self.assertEquals(pari.lindep(['[1,0,0]~', '[0,1,0]~', '[1,1,0]~']), '[1, 1, -1]~')
        self.assertEquals(pari.lindep(['[1,0,0]~', '[0,1,0]~', '[1,1,1]~']), '[]~')
        with self.assertRaises(PariError) as context:
            pari.lindep(['[1,0,0]~', [0, 1, 0], [1, 1, 0]])
        self.assertTrue('incorrect type in lindep (t_VEC)' in str(context.exception))
        self.assertEquals(pari.lindep(['[1,0,0]~', '[0,1,0]~', '[1,1,0]~']), '[1, 1, -1]~')

    def test_seralgdep(self):
        z = pari.sqrt('1+5*y+y^2+y^3');
        self.assertEquals(pari.seralgdep(z, 2, 3), 'x^2 + (-y^3 - y^2 - 5*y - 1)')
        self.assertEquals(pari.seralgdep(z, 2, 2), '0')
        self.assertEquals(pari.seralgdep('1/(1-y+O(y^5))', 1, 1), '(-y + 1)*x - 1')
        self.assertEquals(pari.seralgdep('1+5*y+O(y^3)', 1, 10), '-x + (5*y + 1)')

    def test_algdep(self):
        self.assertEquals(pari.algdep(1, 0), '1')
        with self.assertRaises(PariError) as context:
            pari.algdep(1, -1)
        self.assertTrue('domain error in algdep: degree < 0' in str(context.exception))
        z = pari.sqrt('2+O(7^4)');
        self.assertEquals(pari.algdep(z, 2), 'x^2 - 2')


"""**** Original expected results ****

[-1, -1, 1]~
[1, -2]~
[1, -2, 1]~
[y, y, -1, -y^2]~
x^2 + (-y^3 - y^2 - 5*y - 1)
0
(-y + 1)*x - 1
-x + (5*y + 1)
[]~
[1]~
[]~
[]~
1
  ***   at top-level: algdep(1,-1)
  ***                 ^------------
  *** algdep: domain error in algdep: degree < 0
x^2 - 2
[Mod(0, E^3), Mod(0, E^3), Mod(0, E^3)]~
[1, 1, -1]~
[1, 1, -1]~
[]~
  ***   at top-level: lindep([[1,0,0]~,[0,
  ***                 ^--------------------
  *** lindep: incorrect type in lindep (t_VEC).
[1, 1, -1]~

"""
