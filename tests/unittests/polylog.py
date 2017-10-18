# -*- coding: utf-8 -*-
# This file was generated by tests_generator.py
# Generated the 09/21/2017

"""Original pari/GP test file polylog :
default(realprecision,38);
polylog(3,0.9)
polylog(2,3.9)
polylog(3,3.9)
polylog(2,Mod(x,x^2+1))
polylog(2,[0.5,0.6])
polylog(2,x+O(x^5))
polylog(2,1/2+x+O(x^5))
dilog(-4)
polylog(2,1+I,1)
polylog(1,2,3)
localbitprec(320);bitprecision(dilog(2.0))

\\errors
polylog(3,2,5)
polylog(2,Mod(1,2),0)
polylog(3,"",0)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestPolylog(unittest.TestCase):
    def test_polylog(self):
        pari.set_real_precision(38)
        self.assertEquals(str(pari.polylog(3, '0.9')), '1.0496589501864398696458324932101000704')
        self.assertEquals(str(pari.polylog(2, '3.9')), '2.0886953792151632708518141489041442185 - 4.275633941038' +
                          '7621770489264556951963565*I')
        self.assertEquals(str(pari.polylog(3, '3.9')), '4.3226178452644705784020044544722613393 - 2.909518771772' +
                          '2594640746948896647103179*I')
        self.assertEquals(str(pari.polylog(2, pari.Mod('x', 'x^2+1'), precision=128)), '[-0.20561675835602830455905189583075314' +
                          '866 - 0.91596559417721901505460351493238411074*I, -0.20561675835602830455905189583075' +
                          '314866 + 0.91596559417721901505460351493238411074*I]~')
        self.assertEquals(str(pari.polylog(2, ['0.5', '0.6'])), '[0.58224052646501250590265632015968010874, 0.72' +
                          '758630771633338951353629684048110789]')
        self.assertEquals(str(pari.polylog(2, 'x+O(x^5)')), 'x + 1/4*x^2 + 1/9*x^3 + 1/16*x^4 + O(x^5)')
        self.assertEquals(str(pari.polylog(2, '1/2 + x + O(x^5)', precision=128)), '0.58224052646501250590265632015968010874 + ' +
                          '1.3862943611198906188344642429163531362*x + 0.61370563888010938116553575708364686385*' +
                          'x^2 + 0.51505914815985415844595232388847084820*x^3 + 0.560744611093552095664404847500' +
                          '62706103*x^4 + O(x^5)')
        self.assertEquals(str(pari.dilog(-4, precision=128)), '-2.3699397969983658319855374253503230488')
        self.assertEquals(str(pari.polylog(2, '1+I', 1, precision=128)), '0.91596559417721901505460351493238411077')
        self.assertEquals(str(pari.polylog(1, 2, 3, precision=128)), '0.34657359027997265470861606072908828404')
        pari.set_real_precision_bits(320);
        self.assertEquals(pari.bitprecision(pari.dilog('2.0')), '320')
    def test_polylog_error_cases(self):
        with self.assertRaises(PariError) as context:
            pari.polylog(3, 2, 5)
        self.assertTrue('invalid flag in polylog' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.polylog(2, pari.Mod(1, 2), 0)
        self.assertTrue('sorry, padic polylogarithm is not yet implemented' in str(context.exception))
        with self.assertRaises(PariError) as context:
            pari.polylog(3, '""', 0)
        self.assertTrue('incorrect type in gpolylog (t_STR)' in str(context.exception))

"""**** Original expected results ****

1.0496589501864398696458324932101000704
2.0886953792151632708518141489041442185 - 4.27563394103876217704892645569519
63565*I
4.3226178452644705784020044544722613393 - 2.90951877177225946407469488966471
03179*I
[-0.20561675835602830455905189583075314866 - 0.91596559417721901505460351493
238411074*I, -0.20561675835602830455905189583075314866 + 0.91596559417721901
505460351493238411074*I]~
[0.58224052646501250590265632015968010874, 0.7275863077163333895135362968404
8110789]
x + 1/4*x^2 + 1/9*x^3 + 1/16*x^4 + O(x^5)
0.58224052646501250590265632015968010874 + 1.3862943611198906188344642429163
531362*x + 0.61370563888010938116553575708364686385*x^2 + 0.5150591481598541
5844595232388847084820*x^3 + 0.56074461109355209566440484750062706103*x^4 + 
O(x^5)
-2.3699397969983658319855374253503230488
0.91596559417721901505460351493238411077
0.34657359027997265470861606072908828404
320
  ***   at top-level: polylog(3,2,5)
  ***                 ^--------------
  *** polylog: invalid flag in polylog.
  ***   at top-level: polylog(2,Mod(1,2),0
  ***                 ^--------------------
  *** polylog: sorry, padic polylogarithm is not yet implemented.
  ***   at top-level: polylog(3,"",0)
  ***                 ^---------------
  *** polylog: incorrect type in gpolylog (t_STR).

"""
