# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file mathnf :
\e
mathnf([0,2])
mathnf([0,2], 1)
mathnf([0,x])
mathnf([0,x], 1)
mathnf([x,x^2+1; x^3+x+1, x+2]*Mod(1,5))
v=[116085838, 181081878, 314252913,10346840];
[H,U]=mathnf(v, 1); [v*U, norml2(U)]
[H,U]=mathnf(v, 5); [v*U, norml2(U)]
mathnf([])
mathnf([],1)
mathnf([;])
mathnf([;],1)
mathnfmodid(matrix(0,2), [])
mathnfmodid([0,7;-1,0;-1,-1], [6,2,2])

matsolvemod([;],[]~,[]~,1)
matsolvemod([;],[],[]~,1)
matsolvemod([;],[]~,[],1)
matsolvemod([;],1,1,1)
matsolvemod([1,2;3,4],1,2,1)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestMathnf(unittest.TestCase):
    def test_mathnf(self):
        self.assertEqual(pari.mathnf([0, 2]), 'Mat(2)')
        self.assertEqual(pari.mathnf([0, 2], 1), '[Mat(2), [1, 0; 0, 1]]')
        self.assertEqual(pari.mathnf([0, 'x']), 'Mat(x)')
        self.assertEqual(pari.mathnf([0, 'x'], 1), '[Mat(x), [1, 0; 0, 1]]')
        self.assertEqual(str(pari.mathnf('[x,x^2+1; x^3+x+1, x+2]*Mod(1,5)')),
                         '[Mod(1, 5)*x^5 + Mod(2, 5)*x^3 + Mod(4,' +
                         ' 5)*x + Mod(1, 5), Mod(4, 5)*x^4 + Mod(2, 5)*x^3 + Mod(4, 5)*x^2 + Mod(3, 5)*x; 0, 1]')
        v = [116085838, 181081878, 314252913, 10346840];
        U = pari.mathnf(v, 1)[1];
        self.assertEqual(pari.norml2(U), '2833319')
        U = pari.mathnf(v, 5)[1];
        self.assertEqual(pari.norml2(U), '765585180708864230567243002686057927228240493')
        self.assertEqual(pari.mathnf('[]'), '[;]')
        self.assertEqual(pari.mathnf('[]', 1), '[[;], [;]]')
        self.assertEqual(pari.mathnf('[;]'), '[;]')
        self.assertEqual(pari.mathnf('[;]', 1), '[[;], [;]]')

    def test_mathnfmodid(self):
        self.assertEqual(pari.mathnfmodid('[;]', '[]'), '[;]')
        self.assertEqual(pari.mathnfmodid('[0,7;-1,0;-1,-1]', [6, 2, 2]), '[2, 1, 1; 0, 1, 0; 0, 0, 1]')

    def test_matsolvemod(self):
        self.assertEqual(pari.matsolvemod('[;]', '[]~', '[]~', 1), '0')
        with self.assertRaises(PariError) as context:
            pari.matsolvemod('[;]', '[]', '[]~', 1)
        self.assertTrue('incorrect type in gaussmodulo (t_VEC)' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.matsolvemod('[;]', '[]~', '[]', 1)
        self.assertTrue('incorrect type in gaussmodulo (t_VEC)' in str(context.exception))
        self.assertEqual(pari.matsolvemod('[;]', 1, 1, 1), '0')
        self.assertEqual(pari.matsolvemod('[1,2;3,4]', 1, 2, 1), '[[0, 0]~, [-1, 0; 0, 1]]')

"""**** Original expected results ****

   echo = 1 (on)
? mathnf([0,2])

[2]

? mathnf([0,2],1)
[Mat(2), [1, 0; 0, 1]]
? mathnf([0,x])

[x]

? mathnf([0,x],1)
[Mat(x), [1, 0; 0, 1]]
? mathnf([x,x^2+1;x^3+x+1,x+2]*Mod(1,5))

[Mod(1, 5)*x^5 + Mod(2, 5)*x^3 + Mod(4, 5)*x + Mod(1, 5) Mod(4, 5)*x^4 + Mod
(2, 5)*x^3 + Mod(4, 5)*x^2 + Mod(3, 5)*x]

[0 1]

? v=[116085838,181081878,314252913,10346840];
? [H,U]=mathnf(v,1);[v*U,norml2(U)]
[[0, 0, 0, 1], 2833319]
? [H,U]=mathnf(v,5);[v*U,norml2(U)]
[[0, 0, 0, 1], 765585180708864230567243002686057927228240493]
? mathnf([])
[;]
? mathnf([],1)
[[;], [;]]
? mathnf([;])
[;]
? mathnf([;],1)
[[;], [;]]
? mathnfmodid(matrix(0,2),[])
[;]
? mathnfmodid([0,7;-1,0;-1,-1],[6,2,2])

[2 1 1]

[0 1 0]

[0 0 1]

? matsolvemod([;],[]~,[]~,1)
0
? matsolvemod([;],[],[]~,1)
  ***   at top-level: matsolvemod([;],[],[
  ***                 ^--------------------
  *** matsolvemod: incorrect type in gaussmodulo (t_VEC).
? matsolvemod([;],[]~,[],1)
  ***   at top-level: matsolvemod([;],[]~,
  ***                 ^--------------------
  *** matsolvemod: incorrect type in gaussmodulo (t_VEC).
? matsolvemod([;],1,1,1)
0
? matsolvemod([1,2;3,4],1,2,1)
[[0, 0]~, [-1, 0; 0, 1]]

"""
