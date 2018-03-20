# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file norm :
norml2(-1/2)
norml2(quadgen(5))
norml2(quadgen(-3))
normlp(-1, 1)
normlp(-1/2, 1)
normlp(I, 1)

default(realprecision,38);
F = [x->normlp(x,1), x->normlp(x,2), x->normlp(x,2.5), normlp];
{
  for(i=1, #F,
    my(f = F[i]);
    print(f);
    print(f([1,-2,3]));
    print(f([1,-2;-3,4]));
    print(f([[1,2],[3,4],5,6]));
    print(f((1+I) + I*x^2));
    print(f(-quadgen(5)));
    print(f(3+4*I));
  )
}
normlp([95800,217519,414560], 4)
normlp(-1,oo)
normlp(-1,-oo)

"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestNorm(unittest.TestCase):
    def test_norm(self):
        self.assertEqual(pari.norml2('-1/2'), '1/4')
        with self.assertRaises(PariError) as context:
            pari.norml2(pari.quadgen(5))
        self.assertTrue('incorrect type in gnorml2 (t_QUAD)' in str(context.exception))
        self.assertEqual(pari.norml2(pari.quadgen(-3)), '1')
        self.assertEqual(pari.normlp(-1, 1), '1')
        self.assertEqual(pari.normlp('-1/2', 1), '1/2')
        self.assertEqual(pari.normlp('I', 1), '1')

        pari.set_real_precision(38)
        F = [lambda x: pari.normlp(x, 1, precision=128), lambda x: pari.normlp(x, 2, precision=128),
             lambda x: pari.normlp(x, '2.5', precision=128), lambda x: pari.normlp(x, precision=128)];

        res = [['6',
               '10',
               '21',
               '2.4142135623730950488016887242096980786',
               '1.6180339887498948482045868343656381177',
               '5'],
               ['3.7416573867739413855837487323165493018',
               '5.4772255750516611345696978280080213395',
               '9.5393920141694564915262158602322654026',
               '1.7320508075688772935274463415058723670',
               '1.6180339887498948482045868343656381177',
               '5'],
               ['3.4585606563304871862271371438840799750',
               '4.9402040006184485884345102892270748966',
               '8.2976320964215261445777796306034959974',
               '1.6273657035458510939647914767411763647',
               '1.6180339887498948482045868343656381177',
               '5'],
               ['3',
               '4',
               '6',
               '1.4142135623730950488016887242096980786',
               '1.6180339887498948482045868343656381177',
               '5.0000000000000000000000000000000000000']]

        for i in range(0, len(F)):
            f = F[i]
            self.assertEqual(str(f([1, -2, 3])), res[i][0])
            self.assertEqual(str(f('[1,-2;-3,4]')), res[i][1])
            self.assertEqual(str(f([[1, 2], [3, 4], 5, 6])), res[i][2])
            self.assertEqual(str(f('(1+I) + I*x^2')), res[i][3])
            self.assertEqual(str(f(-pari.quadgen(5))), res[i][4])
            self.assertEqual(str(f('3+4*I')), res[i][5])

        self.assertEqual(str(pari.normlp([95800, 217519, 414560], 4)), '422481')
        self.assertEqual(str(pari.normlp(-1, 'oo')), '1')
        with self.assertRaises(PariError) as context:
            pari.normlp(-1, '-oo')
        self.assertTrue('domain error in normlp: p <= 0' in str(context.exception))

        pari.set_real_precision(15)
        

"""**** Original expected results ****

1/4
  ***   at top-level: norml2(quadgen(5))
  ***                 ^------------------
  *** norml2: incorrect type in gnorml2 (t_QUAD).
1
1
1/2
1
(x)->normlp(x,1)
6
10
21
2.4142135623730950488016887242096980786
1.6180339887498948482045868343656381177
5
(x)->normlp(x,2)
3.7416573867739413855837487323165493018
5.4772255750516611345696978280080213395
9.5393920141694564915262158602322654026
1.7320508075688772935274463415058723670
1.6180339887498948482045868343656381177
5
(x)->normlp(x,2.5)
3.4585606563304871862271371438840799750
4.9402040006184485884345102892270748966
8.2976320964215261445777796306034959974
1.6273657035458510939647914767411763647
1.6180339887498948482045868343656381177
5
normlp
3
4
6
1.4142135623730950488016887242096980786
1.6180339887498948482045868343656381177
5.0000000000000000000000000000000000000
422481
1
  ***   at top-level: normlp(-1,-oo)
  ***                 ^--------------
  *** normlp: domain error in normlp: p <= 0

"""
