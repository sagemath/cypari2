# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file minmax :
v = [-3,7,-2,11];
obj = [1, v, Vecsmall(v), [-3,7;-2,11]];

{
for (i = 1, #obj,
  my (o = obj[i], u,v);
  vecmin(o, &u);
  vecmax(o, &v);
  print(i, ": ", [vecmax(o), vecmin(o), u, v]);
)
}

"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestMinmax(unittest.TestCase):
    def test_minmax(self):
        v = [-3,7,-2,11];
        obj = [1, v, pari.Vecsmall(v), '[-3,7;-2,11]'];

        res = (('1', '1'), ('11', '-3'), ('11', '-3'), ('11', '-3'))
        for i in range(0, len(obj)):
          o = pari(obj[i])
          self.assertEquals((str(o.vecmax()), str(o.vecmin())), res[i])


"""**** Original expected results ****

1: [1, 1, 0, 0]
2: [11, -3, 1, 4]
3: [11, -3, 1, 4]
4: [11, -3, [1, 1], [2, 2]]

"""
