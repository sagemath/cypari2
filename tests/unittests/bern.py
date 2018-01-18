# -*- coding: utf-8 -*-

"""Original pari/GP test file bern :
bernfrac(0);
bernfrac(1);
for(k = 1, 20, print(bernfrac(k)));
for(k = 0, 5, print(bernpol(k)));
bernfrac(-1)
bernreal(-1)
bernpol(-1)
bernvec(30)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestBern(unittest.TestCase):
    def test_bern(self):
        pari.bernfrac(0);
        pari.bernfrac(1);

        t = ('-1/2', '1/6', '0', '-1/30', '0', '1/42', '0', '-1/30', '0', '5/66', '0', '-691/2730',
             '0', '7/6', '0', '-3617/510', '0', '43867/798', '0', '-174611/330')
        for k in range(1, 21):
            self.assertEquals(pari.bernfrac(k), t[k-1])

        t = ('1', 'x - 1/2', 'x^2 - x + 1/6', 'x^3 - 3/2*x^2 + 1/2*x', 'x^4 - 2*x^3 + x^2 - 1/30',
             'x^5 - 5/2*x^4 + 5/3*x^3 - 1/6*x')
        for k in range(0, 6):
            self.assertEquals(pari.bernpol(k), t[k])

        with self.assertRaises(PariError) as context:
            pari.bernfrac(-1)
        self.assertTrue('domain error in bernfrac: index < 0' in str(context.exception))

        with self.assertRaises(PariError) as context:
            pari.bernreal(-1)
        self.assertTrue('domain error in bernreal: index < 0' in str(context.exception))

        with self.assertRaises(PariError) as context:
            pari.bernpol(-1)

        self.assertTrue('domain error in bernpol: index < 0' in str(context.exception))

    def test_bernvec(self):
        self.assertEquals(pari.bernvec(30), '[1, 1/6, -1/30, 1/42, -1/30, 5/66, -691/2730, 7/6, -3617/510, 43867/798,' +
                          ' -174611/330, 854513/138, -236364091/2730, 8553103/6, -23749461029/870, 8615841276005/1432' +
                          '2, -7709321041217/510, 2577687858367/6, -26315271553053477373/1919190, 2929993913841559/6,' +
                          ' -261082718496449122051/13530, 1520097643918070802691/1806, -27833269579301024235023/690, ' +
                          '596451111593912163277961/282, -5609403368997817686249127547/46410, 49505720524107964821247' +
                          '7525/66, -801165718135489957347924991853/1590, 29149963634884862421418123812691/798, -2479' +
                          '392929313226753685415739663229/870, 84483613348880041862046775994036021/354, -121523314048' +
                          '3755572040304994079820246041491/56786730]')
