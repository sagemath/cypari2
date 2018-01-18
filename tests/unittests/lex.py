# -*- coding: utf-8 -*-

"""Original pari/GP test file lex :
v = [0, 2, [1,2], [1,2;3,4], [1,0;1,2], [1,2,3]~, [1,2,3;4,5,6]];

isvec(x) = type(x) == "t_VEC" || type(x) == "t_COL";
{
  for (i = 1, #v,
    for (j = i, #v,
      s = lex(v[i],v[j]);
      print([i,j,s]);
      if (s != -lex(v[j], v[i]), error(2));
      if (isvec(v[i]) && lex(Vecsmall(v[i]), v[j]) != s, error(3));
      if (isvec(v[j]) && lex(v[i], Vecsmall(v[j])) != s, error(4));

    )
  );
}

v = Vecsmall([1,2,3]);
lex(v, [1,2,3])
lex(v, [1,2])
lex(v, [1,2,4])
lex(v, [4,2,3])
lex(v, [0,2,3])
lex(v, [[1,2,3],2,3])
lex(v, [[0,2,3],2,3])
lex(v, [[],2,3])
lex(v, [Vecsmall([]),2,3])
lex(v, [Vecsmall(1),2,3])
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestLex(unittest.TestCase):
    def test_lex(self):
        v = [0, 2, [1, 2], '[1,2;3,4]', '[1,0;1,2]', '[1,2,3]~', '[1,2,3;4,5,6]'];

        def isvec(x):
            return pari.type(x) == "t_VEC" or pari.type(x) == "t_COL"

        l = ['[1, 1, 0]',
             '[1, 2, -1]',
             '[1, 3, -1]',
             '[1, 4, -1]',
             '[1, 5, -1]',
             '[1, 6, -1]',
             '[1, 7, -1]',
             '[2, 2, 0]',
             '[2, 3, 1]',
             '[2, 4, 1]',
             '[2, 5, 1]',
             '[2, 6, 1]',
             '[2, 7, 1]',
             '[3, 3, 0]',
             '[3, 4, -1]',
             '[3, 5, 1]',
             '[3, 6, -1]',
             '[3, 7, -1]',
             '[4, 4, 0]',
             '[4, 5, 1]',
             '[4, 6, 1]',
             '[4, 7, -1]',
             '[5, 5, 0]',
             '[5, 6, -1]',
             '[5, 7, -1]',
             '[6, 6, 0]',
             '[6, 7, -1]',
             '[7, 7, 0]']
        k = 0
        for i in range(0, len(v)):
            for j in range(i, len(v)):
                s = pari.lex(v[i], v[j]);
                self.assertEquals(str([i + 1, j + 1, s]), l[k]);
                self.assertEquals(s, -pari.lex(v[j], v[i]))
                if isvec(v[j]):
                    self.assertEquals(s, pari.lex(pari.Vecsmall(v[i]), v[j]))
                    self.assertEquals(s, pari.lex(v[i], pari.Vecsmall(v[j])))
                k += 1

        v = pari.Vecsmall([1, 2, 3]);
        pari.lex(v, [1, 2, 3])
        pari.lex(v, [1, 2])
        pari.lex(v, [1, 2, 4])
        pari.lex(v, [4, 2, 3])
        pari.lex(v, [0, 2, 3])
        pari.lex(v, [[1, 2, 3], 2, 3])
        pari.lex(v, [[0, 2, 3], 2, 3])
        pari.lex(v, [[], 2, 3])
        pari.lex(v, [pari.Vecsmall([]), 2, 3])
        pari.lex(v, [pari.Vecsmall(1), 2, 3])

"""**** Original expected results ****

[1, 1, 0]
[1, 2, -1]
[1, 3, -1]
[1, 4, -1]
[1, 5, -1]
[1, 6, -1]
[1, 7, -1]
[2, 2, 0]
[2, 3, 1]
[2, 4, 1]
[2, 5, 1]
[2, 6, 1]
[2, 7, 1]
[3, 3, 0]
[3, 4, -1]
[3, 5, 1]
[3, 6, -1]
[3, 7, -1]
[4, 4, 0]
[4, 5, 1]
[4, 6, 1]
[4, 7, -1]
[5, 5, 0]
[5, 6, -1]
[5, 7, -1]
[6, 6, 0]
[6, 7, -1]
[7, 7, 0]
0
1
-1
-1
1
-1
1
1
1
-1

"""
