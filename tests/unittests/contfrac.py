# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file contfrac :
contfrac(1,[],-1)
contfracpnqn(Vecsmall([]))
contfracpnqn([])
contfracpnqn([],0)
contfracpnqn([],1)
contfracpnqn([2])
contfracpnqn([2],0)
contfracpnqn([2],1)
v=[1,2,3];
contfracpnqn(v)
contfracpnqn(v,0)
contfracpnqn(v,1)
contfracpnqn(v,2)
v=[1,2,3;4,5,6];
contfracpnqn(v)
contfracpnqn(v,0)
contfracpnqn(v,1)
contfracpnqn(v,2)

s=exp(x);
contfracinit(s,0)
contfracinit(s,1)
contfracinit(s,2)
e=contfracinit([])
contfraceval(e,1)
e=contfracinit(s)
contfraceval(e,1,10)
contfraceval(e,1, 8)
contfraceval(e,1, 6)
contfraceval(e,1)
contfracinit([1,2,3])
contfracinit(Pol(0))
contfracinit(1);
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestContfrac(unittest.TestCase):
    def test_contfrac(self):
        with self.assertRaises(PariError) as context:
            pari.contfrac(1, '[]', -1)
        self.assertTrue('domain error in contfrac: nmax < 0' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.contfracpnqn(pari.Vecsmall('[]'))
        self.assertTrue('incorrect type in pnqn (t_VECSMALL)' in str(context.exception))
        self.assertEqual(pari.contfracpnqn('[]'), '[1, 0; 0, 1]')
        self.assertEqual(pari.contfracpnqn('[]', 0), '[;]')
        self.assertEqual(pari.contfracpnqn('[]', 1), '[;]')
        self.assertEqual(pari.contfracpnqn([2]), '[2, 1; 1, 0]')
        self.assertEqual(pari.contfracpnqn([2], 0), '[2; 1]')
        self.assertEqual(pari.contfracpnqn([2], 1), '[2; 1]')

        v = [1, 2, 3];
        self.assertEqual(pari.contfracpnqn(v), '[10, 3; 7, 2]')
        self.assertEqual(pari.contfracpnqn(v, 0), '[1; 1]')
        self.assertEqual(pari.contfracpnqn(v, 1), '[1, 3; 1, 2]')
        self.assertEqual(pari.contfracpnqn(v, 2), '[1, 3, 10; 1, 2, 7]')

        v = '[1,2,3;4,5,6]';
        self.assertEqual(pari.contfracpnqn(v), '[144, 22; 33, 5]')
        self.assertEqual(pari.contfracpnqn(v, 0), '[4; 1]')
        self.assertEqual(pari.contfracpnqn(v, 1), '[4, 22; 1, 5]')
        self.assertEqual(pari.contfracpnqn(v, 2), '[4, 22, 144; 1, 5, 33]')

        s = pari.exp('x');
        self.assertEqual(pari.contfracinit(s, 0), '[[], []]')
        self.assertEqual(pari.contfracinit(s, 1), '[[-1], []]')
        self.assertEqual(pari.contfracinit(s, 2), '[[-1], [1/2]]')

        e = pari.contfracinit('[]')
        self.assertEqual(pari.contfraceval(e, 1), '[[], []]')

        e = pari.contfracinit(s)
        self.assertEquals(e, '[[-1, 1/3, 1/15, 1/35, 1/63, 1/99, 1/143, 1/195], [1/2, 1/36, 1/100, 1/196, ' +
                          '1/324, 1/484, 1/676, 1/900]]')

        with self.assertRaises(PariError) as context:
            pari.contfraceval(e, 1, 10)
        self.assertTrue('non-existent component in contfraceval: index > 8' in str(context.exception))
        self.assertEqual(pari.contfraceval(e, 1, 8), '410105312/150869313')
        self.assertEqual(pari.contfraceval(e, 1, 6), '517656/190435')
        self.assertEqual(pari.contfraceval(e, 1), '410105312/150869313')
        self.assertEquals(pari.contfracinit([1, 2, 3]), '[[-2], [1]]')
        self.assertEqual(pari.contfracinit(pari.Pol(0)), '[[], []]')
        with self.assertRaises(PariError) as context:
            pari.contfracinit(1);
        self.assertTrue('incorrect type in contfracinit (t_INT)' in str(context.exception))

"""**** Original expected results ****

  ***   at top-level: contfrac(1,[],-1)
  ***                 ^-----------------
  *** contfrac: domain error in contfrac: nmax < 0
  ***   at top-level: contfracpnqn(Vecsmal
  ***                 ^--------------------
  *** contfracpnqn: incorrect type in pnqn (t_VECSMALL).

[1 0]

[0 1]

[;]
[;]

[2 1]

[1 0]


[2]

[1]


[2]

[1]


[10 3]

[ 7 2]


[1]

[1]


[1 3]

[1 2]


[1 3 10]

[1 2  7]


[144 22]

[ 33  5]


[4]

[1]


[4 22]

[1  5]


[4 22 144]

[1  5  33]

[[], []]
[[-1], []]
[[-1], [1/2]]
[[], []]
0
[[-1, 1/3, 1/15, 1/35, 1/63, 1/99, 1/143, 1/195], [1/2, 1/36, 1/100, 1/196, 
1/324, 1/484, 1/676, 1/900]]
  ***   at top-level: contfraceval(e,1,10)
  ***                 ^--------------------
  *** contfraceval: non-existent component in contfraceval: index > 8
410105312/150869313
517656/190435
410105312/150869313
[[-2], [1]]
[[], []]
  ***   at top-level: contfracinit(1)
  ***                 ^---------------
  *** contfracinit: incorrect type in contfracinit (t_INT).

"""
