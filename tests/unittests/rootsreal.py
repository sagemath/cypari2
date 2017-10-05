# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file rootsreal :
default(realprecision,38);
T=x^3-6*x^2+11*x-6;
polrootsreal(T)
polrootsreal(T, [-oo,3/2])
polrootsreal(T, [3/2,6])
polrootsreal(T, [-oo,+oo])
polrootsreal(T, [2,3])
polrootsreal(T, [1,2])
polsturm(T, [-oo,3/2])
polsturm(T, [3/2,6])
polsturm(T, [-oo,+oo])
polsturm(T, [2,3])
polsturm(T, [1,2])
polsturm(T, [1,+oo])
polsturm(T, 2,3)
polsturm(T, 2.,3)
polsturm(T,,2)
polrootsreal(x^10 + 23*x^9 + 19*x^8 + 18*x^7 + 39*x^6 + 41*x^5 + 46*x^4 + 24*x^3 - 4*x^2 + 2*x + 42)
polrootsreal(polchebyshev(9))
polrootsreal(polchebyshev(10))
polrootsreal(x^0)
polrootsreal(1)
polrootsreal(0)
polrootsreal(Pol(0))
polrootsreal(Mod(1,2))

polroots(T*x+0.)
polroots(1)
polrootsreal(T,[1,1])
polrootsreal(T,[0,0])
polsturm(T,[1,1])
polsturm(T,[2,1])

U=(x^2-1)*(x-2);
polsturm(U)
polsturm(U,[-oo,1])
polsturm(U,[-1,+oo])

polrootsreal(x,[1,2])
polrootsreal(x,[-2,-1])
polrootsreal(x,[-1,1])

polrootsreal(x^3-2)
polrootsreal(x^3+2)
\\#1605
polsturm(33*x^2-4*x-1)
polrootsreal(4*x)
polsturm(-4*x)
polsturm((x^4-2)^2)

\\#1807
T=x^3+x^2-x+2;
polrootsreal(T)
polsturm(T)
polsturm(T,[-3,-1])
polsturm(T,[-2,-1])
polsturm(T,[-oo,-2])
polsturm(T,[-2,oo])
T=4*x^3-2*x^2-x-1;
polsturm(T,[0,oo])
polsturm(T,[0,1])
polsturm(T,[0,2])
polsturm(T,[1,3])

\\#1808
polrootsreal(3*x^3-4*x^2+3*x-1)

\\#1809
polrootsreal(x^3-3*x^2-3*x+2)

\\#1810
polrootsreal(x^3-x^2)
polrootsreal((x^3-x^2)*(x-2)^3*(x-3)^2)

default(realprecision,19);
#polroots((x+1)^2 * (x-1)^7 * (x^2-x+1)^5 * 1.0)

\\#1884
default(realprecision,38);
polsturm(x^2-1,[-1,1])
polrootsreal(x^2-1,[-1,1])
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestRootsreal(unittest.TestCase):
    def setUp(self):
        pari.set_real_precision(38)

    def tearDown(self):
        pari.set_real_precision(15)

    def test_rootsreal(self):
        T = 'x^3-6*x^2+11*x-6';
        self.assertEquals(pari.polrootsreal(T), '[1.0000000000000000000000000000000000000, 2.00000000000000000000'
                                                '00000000000000000, 3.0000000000000000000000000000000000000]~')
        self.assertEquals(pari.polrootsreal(T, ['-oo', '3/2']), '[1.0000000000000000000000000000000000000]~')
        self.assertEquals(pari.polrootsreal(T, ['3/2', 6]),
                          '[2.0000000000000000000000000000000000000, 3.0000000000000000000000000000000000000]~')
        self.assertEquals(pari.polrootsreal(T, ['-oo', '+oo']),
                          '[1.0000000000000000000000000000000000000, 2.0000000000000000000000000000000000000, '
                          '3.0000000000000000000000000000000000000]~')
        self.assertEquals(pari.polrootsreal(T, [2, 3]),
                          '[2.0000000000000000000000000000000000000, 3.0000000000000000000000000000000000000]~')
        self.assertEquals(pari.polrootsreal(T, [1, 2]),
                          '[1.0000000000000000000000000000000000000, 2.0000000000000000000000000000000000000]~')

        self.assertEquals(str(pari.polsturm(T, ['-oo', '3/2'])), '1')
        self.assertEquals(str(pari.polsturm(T, ['3/2', 6])), '2')
        self.assertEquals(str(pari.polsturm(T, ['-oo', '+oo'])), '3')
        self.assertEquals(str(pari.polsturm(T, [2, 3])), '2')
        self.assertEquals(str(pari.polsturm(T, [1, 2])), '2')
        self.assertEquals(str(pari.polsturm(T, [1, '+oo'])), '3')
        self.assertEquals(str(pari.polsturm(T, 2, 3)), '2')
        self.assertEquals(str(pari.polsturm(T, '2.', 3)), '2')
        self.assertEquals(str(pari.polsturm(T, None, 2)), '2')
        self.assertEquals(str(pari.polrootsreal('x^10 + 23*x^9 + 19*x^8 + 18*x^7 + 39*x^6 + 41*x^5 + 46*x^4 + 24*x^3'
                                            ' - 4*x^2 + 2*x + 42', precision=127)),
                          '[-22.176420046821213834911725420609849287, -1.2204011038823372357354593544256902868]~')
        self.assertEquals(str(pari.polrootsreal(pari.polchebyshev(9), precision=127)),
                          '[-0.98480775301220805936674302458952301367, -0.86602540378443864676372317075293618347, -' +
                          '0.64278760968653932632264340990726343291, -0.34202014332566873304409961468225958076, 0.E' +
                          '-38, 0.34202014332566873304409961468225958076, 0.64278760968653932632264340990726343291,' +
                          ' 0.86602540378443864676372317075293618347, 0.98480775301220805936674302458952301367]~')
        self.assertEquals(str(pari.polrootsreal(pari.polchebyshev(10), precision=127)),
                          '[-0.98768834059513772619004024769343726076, -0.89100652418836786235970957141362631277, -' +
                          '0.70710678118654752440084436210484903928, -0.45399049973954679156040836635787119898, -0.' +
                          '15643446504023086901010531946716689231, 0.15643446504023086901010531946716689231, 0.4539' +
                          '9049973954679156040836635787119898, 0.70710678118654752440084436210484903928, 0.89100652' +
                          '418836786235970957141362631277, 0.98768834059513772619004024769343726076]~')
        self.assertEquals(str(pari.polrootsreal('x^0', precision=127)), '[]~')
        self.assertEquals(str(pari.polrootsreal(1, precision=127)), '[]~')

        with self.assertRaises(PariError) as context:
            pari.polrootsreal(0, precision=127)
        self.assertTrue('zero polynomial in realroots' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.polrootsreal(pari.Pol(0), precision=127)
        self.assertTrue('zero polynomial in realroots' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.polrootsreal(pari.Mod(1, 2), precision=127)
        self.assertTrue('incorrect type in realroots (t_INTMOD)' in str(context.exception))

        self.assertEquals(pari.polroots('(x^3-6*x^2+11*x-6)*x+0.'),
                          '[0.E-38 + 0.E-38*I, 1.0000000000000000000000000000000000000 + 0.E-38*I, 2.00000000000000' +
                          '00000000000000000000000 + 0.E-38*I, 3.0000000000000000000000000000000000000 + 0.E-38*I]~')
        self.assertEquals(pari.polroots(1), '[]~')
        self.assertEquals(str(pari.polrootsreal(T, [1, 1], precision=127)),
                          '[1.0000000000000000000000000000000000000]~')
        self.assertEquals(str(pari.polrootsreal(T, [0, 0], precision=127)), '[]~')
        self.assertEquals(str(pari.polsturm(T, [1, 1])), '1')
        self.assertEquals(str(pari.polsturm(T, [2, 1])), '0')

        U = '(x^2-1)*(x-2)';
        self.assertEquals(str(pari.polsturm(U)), '3')
        self.assertEquals(str(pari.polsturm(U, ['-oo', 1])), '2')
        self.assertEquals(str(pari.polsturm(U, [-1, '+oo'])), '3')

        self.assertEquals(str(pari.polrootsreal('x', [1, 2])), '[]~')
        self.assertEquals(str(pari.polrootsreal('x', [-2, -1])), '[]~')
        self.assertEquals(str(pari.polrootsreal('x', [-1, 1], precision=127)), '[0.E-38]~')

        self.assertEquals(str(pari.polrootsreal('x^3-2', precision=127)), '[1.2599210498948731647672106072782283506]~')
        self.assertEquals(str(pari.polrootsreal('x^3+2', precision=127)), '[-1.2599210498948731647672106072782283506]~')

        # #1605
        self.assertEquals(str(pari.polsturm('33*x^2-4*x-1')), '2')
        self.assertEquals(str(pari.polrootsreal('4*x', precision=127)), '[0.E-38]~')
        self.assertEquals(str(pari.polsturm('-4*x')), '1')
        with self.assertRaises(PariError) as context:
            pari.polsturm('(x^4-2)^2')
        self.assertTrue('domain error in polsturm: issquarefree(pol) = 0' in str(context.exception))

        # #1807
        T = 'x^3+x^2-x+2';
        self.assertEquals(str(pari.polrootsreal(T, precision=127)), '[-2.0000000000000000000000000000000000000]~')
        self.assertEquals(str(pari.polsturm(T)), '1')
        self.assertEquals(str(pari.polsturm(T, [-3, -1])), '1')
        self.assertEquals(str(pari.polsturm(T, [-2, -1])), '1')
        self.assertEquals(str(pari.polsturm(T, ['-oo', -2])), '1')
        self.assertEquals(str(pari.polsturm(T, [-2, 'oo'])), '1')

        T = '4*x^3-2*x^2-x-1';
        self.assertEquals(str(pari.polsturm(T, [0, 'oo'])), '1')
        self.assertEquals(str(pari.polsturm(T, [0, 1])), '1')
        self.assertEquals(str(pari.polsturm(T, [0, 2])), '1')
        self.assertEquals(str(pari.polsturm(T, [1, 3])), '1')

        # #1808
        self.assertEquals(str(pari.polrootsreal('3*x^3-4*x^2+3*x-1', precision=127)),
                              '[0.59441447601624956642908249516963028371]~')

        # #1809
        self.assertEquals(str(pari.polrootsreal('x^3-3*x^2-3*x+2', precision=127)),
                          '[-1.1451026912004224304268100262663119669, 0.47602360291813403446915767711979045497, '
                          '3.6690790882822883959576523491465215119]~')

        # #1810
        self.assertEquals(str(pari.polrootsreal('x^3-x^2', precision=127)),
                          '[0.E-38, 0.E-38, 1.0000000000000000000000000000000000000]~')
        self.assertEquals(str(pari.polrootsreal('(x^3-x^2)*(x-2)^3*(x-3)^2', precision=127)),
                          '[0.E-38, 0.E-38, 1.0000000000000000000000000000000000000, 2.00000000000000000000' +
                          '00000000000000000, 2.0000000000000000000000000000000000000, 2.000000000000000000' +
                          '0000000000000000000, 3.0000000000000000000000000000000000000, 3.0000000000000000' +
                          '000000000000000000000]~')

        pari.set_real_precision(19)
        self.assertEquals(len(pari.polroots('(x+1)^2 * (x-1)^7 * (x^2-x+1)^5 * 1.0')), 19)

        # #1884
        pari.set_real_precision(38)
        self.assertEquals(str(pari.polsturm('x^2-1', [-1, 1])), '2')
        self.assertEquals(str(pari.polrootsreal('x^2-1', [-1, 1], precision=127)),
                          '[-1.0000000000000000000000000000000000000, 1.0000000000000000000000000000000000000]~')

"""**** Original expected results ****

[1.0000000000000000000000000000000000000, 2.00000000000000000000000000000000
00000, 3.0000000000000000000000000000000000000]~
[1.0000000000000000000000000000000000000]~
[2.0000000000000000000000000000000000000, 3.00000000000000000000000000000000
00000]~
[1.0000000000000000000000000000000000000, 2.00000000000000000000000000000000
00000, 3.0000000000000000000000000000000000000]~
[2.0000000000000000000000000000000000000, 3.00000000000000000000000000000000
00000]~
[1.0000000000000000000000000000000000000, 2.00000000000000000000000000000000
00000]~
1
2
3
2
2
3
2
2
2
[-22.176420046821213834911725420609849287, -1.220401103882337235735459354425
6902868]~
[-0.98480775301220805936674302458952301367, -0.86602540378443864676372317075
293618347, -0.64278760968653932632264340990726343291, -0.3420201433256687330
4409961468225958076, 0.E-38, 0.34202014332566873304409961468225958076, 0.642
78760968653932632264340990726343291, 0.8660254037844386467637231707529361834
7, 0.98480775301220805936674302458952301367]~
[-0.98768834059513772619004024769343726076, -0.89100652418836786235970957141
362631277, -0.70710678118654752440084436210484903928, -0.4539904997395467915
6040836635787119898, -0.15643446504023086901010531946716689231, 0.1564344650
4023086901010531946716689231, 0.45399049973954679156040836635787119898, 0.70
710678118654752440084436210484903928, 0.891006524188367862359709571413626312
77, 0.98768834059513772619004024769343726076]~
[]~
[]~
  ***   at top-level: polrootsreal(0)
  ***                 ^---------------
  *** polrootsreal: zero polynomial in realroots.
  ***   at top-level: polrootsreal(Pol(0))
  ***                 ^--------------------
  *** polrootsreal: zero polynomial in realroots.
  ***   at top-level: polrootsreal(Mod(1,2
  ***                 ^--------------------
  *** polrootsreal: incorrect type in realroots (t_INTMOD).
[0.E-38 + 0.E-38*I, 1.0000000000000000000000000000000000000 + 0.E-38*I, 2.00
00000000000000000000000000000000000 + 0.E-38*I, 3.00000000000000000000000000
00000000000 + 0.E-38*I]~
[]~
[1.0000000000000000000000000000000000000]~
[]~
1
0
3
2
3
[]~
[]~
[0.E-38]~
[1.2599210498948731647672106072782283506]~
[-1.2599210498948731647672106072782283506]~
2
[0.E-38]~
1
  ***   at top-level: polsturm((x^4-2)^2)
  ***                 ^-------------------
  *** polsturm: domain error in polsturm: issquarefree(pol) = 0
[-2.0000000000000000000000000000000000000]~
1
1
1
1
1
1
1
1
1
[0.59441447601624956642908249516963028371]~
[-1.1451026912004224304268100262663119669, 0.4760236029181340344691576771197
9045497, 3.6690790882822883959576523491465215119]~
[0.E-38, 0.E-38, 1.0000000000000000000000000000000000000]~
[0.E-38, 0.E-38, 1.0000000000000000000000000000000000000, 2.0000000000000000
000000000000000000000, 2.0000000000000000000000000000000000000, 2.0000000000
000000000000000000000000000, 3.0000000000000000000000000000000000000, 3.0000
000000000000000000000000000000000]~
19
2
[-1.0000000000000000000000000000000000000, 1.0000000000000000000000000000000
000000]~

"""
