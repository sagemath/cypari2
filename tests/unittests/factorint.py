# -*- coding: utf-8 -*-

"""Original pari/GP test file factorint :
factorint(-33623546348886051018593728804851,1)
factorint(691160558642,1)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestFactorint(unittest.TestCase):
    def test_factorint(self):
        self.assertEquals(str(pari.factorint(-33623546348886051018593728804851, 1)),
                          '[-1, 1; 3, 5; 73, 1; 181, 1; 223, 1; 293, 2; 4157, 2; 112573, 1; 281191, 1]')
        self.assertEquals(str(pari.factorint(691160558642,1)), '[2, 1; 397, 1; 27031, 1; 32203, 1]')

"""**** Original expected results ****


[    -1 1]

[     3 5]

[    73 1]

[   181 1]

[   223 1]

[   293 2]

[  4157 2]

[112573 1]

[281191 1]


[    2 1]

[  397 1]

[27031 1]

[32203 1]


"""
