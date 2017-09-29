# -*- coding: utf-8 -*-
# Created 09/26/2017

"""Original pari/GP test file list :
L = List();
for (i=1,10^5,listput(L,i))
L = List([1,2,3]);
for (i=1,5000,listinsert(L,i,3))
L = List([1,2,3,3]);
concat(L,5)
concat(1,L)
L = concat(L,L)
listsort(L); L
listsort(L,1); L
listpop(L); L
listpop(L,1); L
\\
L = List([[1,2,3], 2])
L[1][1] = 3
L
L = List([Vecsmall([1,2,3]), 2])
L[1][1] = 3

L = List(); listput(L,1); listpop(L); listpop(L);

matdiagonal(List([0]))
g(L)=for(i=1,5,listput(L,5-i));L;
l=List([10,9,8,7,6,5]); g(l)
l
listkill(l)
listcreate()

subst(List([x,x^2+y]),x,1)
substvec(List([x,y]), [x,y], [y,x])
substpol(List([x^2,x^3]), x^2, y)

getheap()[1]

chinese(List())
chinese(List([Mod(1,3)]))
chinese(List([Mod(0,2),Mod(1,3),Mod(2,5)]))
liftint(List([0,1]))

L = List([1,2,3]);
L[1]
L[1]*=2
L
L[1]=3
L
"""
import unittest
from cypari2 import Pari, PariError
from math import pow

pari = Pari()


class TestList(unittest.TestCase):
    def test_list(self):
        L = pari.List();

        for i in range(1, int(pow(10, 5) + 1)):
            pari.listput(L, i)

        L = pari.List([1, 2, 3]);
        for i in range(1, 5000):
            pari.listinsert(L, i, 3)

        L = pari.List([1, 2, 3, 3]);
        self.assertEquals(pari.concat(L, 5), 'List([1, 2, 3, 3, 5])')
        self.assertEquals(pari.concat(1, L), 'List([1, 1, 2, 3, 3])')
        L = pari.concat(L, L)
        self.assertEquals(L, 'List([1, 2, 3, 3, 1, 2, 3, 3])')
        pari.listsort(L);
        self.assertEquals(L, 'List([1, 1, 2, 2, 3, 3, 3, 3])')
        pari.listsort(L, 1);
        self.assertEquals(L,'List([1, 2, 3])')
        pari.listpop(L);
        self.assertEquals(L, 'List([1, 2])')
        pari.listpop(L, 1);
        self.assertEquals(L, 'List([2])')

        L = pari.List([[1,2,3], 2])
        # L[0][0] = 3
        # self.assertEquals(L, 'List([[3, 2, 3], 2])')
        L = pari.List([pari.Vecsmall([1,2,3]), 2])
        self.assertEquals(L, 'List([Vecsmall([1, 2, 3]), 2])')

        L = pari.List();
        pari.listput(L, 1);
        pari.listpop(L);
        pari.listpop(L);

        # self.assertEquals(pari.matdiagonal(pari.List([0])), '[List([0])]')
        def g(L):
            res = pari.List(L)
            for i in range(1, 6):
                pari.listput(res, 5-i)
            return res

        l = pari.List([10, 9, 8, 7, 6, 5]);
        self.assertEquals(g(l), 'List([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])')
        self.assertEquals(l, 'List([10, 9, 8, 7, 6, 5])')
        pari.listkill(l)
        self.assertEquals(pari.List(), 'List([])')

        self.assertEquals(pari.subst(pari.List(['x', 'x^2+y']), 'x', 1), 'List([1, y + 1])')
        self.assertEquals(pari.substvec(pari.List(['x', 'y']), ['x', 'y'], ['y', 'x']), 'List([y, x])')
        self.assertEquals(pari.substpol(pari.List(['x^2', 'x^3']), 'x^2', 'y'), 'List([y, y*x])')

        self.assertEquals(pari.chinese(pari.List()), 'Mod(0, 1)')
        self.assertEquals(pari.chinese(pari.List([pari.Mod(1, 3)])), 'Mod(1, 3)')
        self.assertEquals(pari.chinese(pari.List([pari.Mod(0, 2), pari.Mod(1, 3), pari.Mod(2, 5)])), 'Mod(22, 30)')
        self.assertEquals(pari.liftint(pari.List([0, 1])), 'List([0, 1])')

        L = pari.List([1, 2, 3]);
        self.assertEquals(L[0], '1')
        # L[1]*=2
        # L
        # L[1]=3
        # L

"""**** Original expected results ****

List([1, 2, 3, 3, 5])
List([1, 1, 2, 3, 3])
List([1, 2, 3, 3, 1, 2, 3, 3])
List([1, 1, 2, 2, 3, 3, 3, 3])
List([1, 2, 3])
List([1, 2])
List([2])
List([[1, 2, 3], 2])
3
List([[3, 2, 3], 2])
List([Vecsmall([1, 2, 3]), 2])
3

[List([0])]

List([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
List([10, 9, 8, 7, 6, 5])
List([])
List([1, y + 1])
List([y, x])
List([y, y*x])
127
Mod(0, 1)
Mod(1, 3)
Mod(22, 30)
List([0, 1])
1
2
List([2, 2, 3])
3
List([3, 2, 3])

"""
