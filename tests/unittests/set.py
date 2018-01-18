# -*- coding: utf-8 -*-

"""Original pari/GP test file set :
Set(Vecsmall([1,2,1,3]))
Set(List([]))
L=List([1,3,1,2,3]);
Set(L)
listsort(L,1); L
Set(1)
a=Set([5,-2,7,3,5,1,x,"1"])
b=Set([7,5,-5,7,2,"1"])
setintersect(a,b)
setisset([-3,5,7,7])
setisset(a)
setminus(a,b)
setsearch(a,3)
setsearch(a,"1")
setsearch(b,3)
setsearch(L,3)
setsearch(1,3)
setunion(a,b)
X = [1,2,3]; Y = [2,3,4];
setbinop((x,y)->x+y, X,Y)
setbinop((x,y)->x+y, X)
setbinop(x->x, X)
"""
import unittest
from cypari2 import Pari, PariError

pari = Pari()


class TestSet(unittest.TestCase):
    def test_set(self):
        self.assertEquals(pari.Set(pari.Vecsmall([1,2,1,3])), '[1, 2, 3]')
        self.assertEquals(pari.Set(pari.List([])), '[]')
        L=pari.List([1, 3, 1, 2, 3]);
        self.assertEquals(pari.Set(L), '[1, 2, 3]')
        pari.listsort(L, 1)
        self.assertEquals(L, 'List([1, 2, 3])')
        self.assertEquals(pari.Set(1), '[1]')
        a = pari.Set([5, -2, 7, 3, 5, 1, 'x', '"1"'])
        b = pari.Set([7, 5, -5, 7, 2, '"1"'])
        self.assertEquals(str(a), '[-2, 1, 3, 5, 7, x, "1"]')
        self.assertEquals(str(b), '[-5, 2, 5, 7, "1"]')
        self.assertEquals(pari.setintersect(a, b), '[5, 7, "1"]')
        self.assertEquals(str(pari.setisset([-3, 5, 7, 7])), '0')
        self.assertEquals(str(pari.setisset(a)), '1')
        self.assertEquals(pari.setminus(a, b), '[-2, 1, 3, x]')
        self.assertEquals(str(pari.setsearch(a, 3)), '3')
        self.assertEquals(str(pari.setsearch(a, '"1"')), '7')
        self.assertEquals(str(pari.setsearch(b, 3)), '0')
        self.assertEquals(str(pari.setsearch(L, 3)), '3')
        with self.assertRaises(PariError) as context:
            pari.setsearch(1, 3)
        self.assertTrue('type in setsearch (t_INT)' in str(context.exception))
        self.assertEquals(pari.setunion(a, b), '[-5, -2, 1, 2, 3, 5, 7, x, "1"]')

        X = [1, 2, 3];
        Y = [2, 3, 4];
        pari.setbinop('(x,y)->x+y', X, Y)
        pari.setbinop('(x,y)->x+y', X)
        with self.assertRaises(PariError) as context:
            pari.setbinop('x->x', X)
        self.assertTrue('incorrect type in setbinop [function needs exactly 2 arguments] (t_CLOSURE)' in
                        str(context.exception))

"""**** Original expected results ****
[1, 2, 3]
[]
[1, 2, 3]
List([1, 2, 3])
[1]
[-2, 1, 3, 5, 7, x, "1"]
[-5, 2, 5, 7, "1"]
[5, 7, "1"]
0
1
[-2, 1, 3, x]
3
7
0
3
  ***   at top-level: setsearch(1,3)
  ***                 ^--------------
  *** setsearch: incorrect type in setsearch (t_INT).
[-5, -2, 1, 2, 3, 5, 7, x, "1"]
[3, 4, 5, 6, 7]
[2, 3, 4, 5, 6]
  ***   at top-level: setbinop(x->x,X)
  ***                 ^----------------
  *** setbinop: incorrect type in setbinop [function needs exactly 2 arguments] (t_CLOSURE).
"""
