"""Exercise precision arguments on both sides of PARI word boundaries."""

import unittest

from cypari2 import Pari


PRECISIONS = (53, 63, 64, 65, 127, 128, 129)


class TestPrecision(unittest.TestCase):
    def setUp(self):
        self.pari = Pari()

    def assert_close(self, actual, expected, bits):
        if isinstance(actual, tuple):
            self.assertEqual(len(actual), len(expected))
            for a, b in zip(actual, expected):
                self.assert_close(a, b, bits)
        elif actual.type() in ('t_VEC', 't_COL', 't_MAT'):
            self.assertEqual(len(actual), len(expected))
            for a, b in zip(actual, expected):
                self.assert_close(a, b, bits)
        else:
            tolerance = self.pari(2) ** (-bits + 10)
            self.assertLessEqual(abs(actual - expected), tolerance * max(1, abs(expected)))

    def test_eigenvectors(self):
        # The first matrix failed in PARI 2.19 at precision=53 before
        # mateigen's wrapper retained word-aligned working precision.
        for matrix in ('[0,1;-2,0]', '[1,2;2,1]'):
            M = self.pari(matrix)
            for bits in PRECISIONS:
                for call in (M.mateigen, lambda **kw: self.pari.mateigen(M, **kw)):
                    with self.subTest(matrix=matrix, bits=bits, call=call):
                        values, vectors = call(flag=1, precision=bits)
                        self.assertEqual(len(values), 2)
                        self.assert_close(M * vectors, vectors * values.matdiagonal(), bits)
                        polynomial = M.charpoly()
                        for value in values:
                            self.assert_close(polynomial.subst('x', value), self.pari(0), bits)

    def test_qr(self):
        M = self.pari('[4,1;1,3]')
        for bits in PRECISIONS:
            with self.subTest(bits=bits):
                Q, R = M.matqr(precision=bits)
                self.assert_close(Q * R, M, bits)
                self.assert_close(Q.mattranspose() * Q, self.pari.matid(2), bits)

    def test_jacobi(self):
        M = self.pari('[4,1;1,3]')
        for bits in PRECISIONS:
            with self.subTest(bits=bits):
                values, vectors = M.qfjacobi(precision=bits)
                self.assert_close(M * vectors, vectors * values.matdiagonal(), bits)
                self.assert_close(vectors.mattranspose() * vectors, self.pari.matid(2), bits)

    def test_cholesky(self):
        M = self.pari('[4,1;1,3]')
        for bits in PRECISIONS:
            with self.subTest(bits=bits):
                R = M.qfcholesky(precision=bits)
                self.assert_close(R.mattranspose() * R, M, bits)

    def test_polynomial_roots(self):
        polynomial = self.pari('x^3-2')
        for bits in PRECISIONS:
            for method, count in (('polroots', 3), ('polrootsreal', 1)):
                with self.subTest(bits=bits, method=method):
                    roots = getattr(polynomial, method)(precision=bits)
                    self.assertEqual(len(roots), count)
                    for root in roots:
                        self.assert_close(polynomial.subst('x', root), self.pari(0), bits)

    def test_transcendental_functions(self):
        # Include generated wrappers and the handwritten bernreal,
        # besselk, eint1, polylog and sqrtn wrappers.
        x = self.pari('1/3')
        cases = {
            'Pi': (), 'Euler': (), 'Catalan': (),
            'acos': (x,), 'acosh': (2,), 'agm': (1, 2), 'airy': (1,),
            'asin': (x,), 'asinh': (x,), 'atan': (x,), 'atanh': (x,),
            'bernreal': (10,), 'besselh1': (1, 2), 'besselh2': (1, 2),
            'besseli': (1, 2), 'besselj': (1, 2), 'besseljh': (1, 2),
            'besseljzero': (1, 1), 'besselk': (1, 2), 'bessely': (1, 2),
            'besselyzero': (1, 1), 'cos': (x,), 'cosh': (x,),
            'cotan': (x,), 'cotanh': (x,), 'dilog': (x,), 'eint1': (1,),
            'ellE': (x,), 'ellK': (x,), 'ellj': (self.pari('I'),),
            'erfc': (x,), 'eta': (self.pari('I'),), 'eulerreal': (10,),
            'exp': (x,), 'expm1': (x,), 'factorial': (10,),
            'gamma': (x,), 'gammah': (x,), 'hypergeom': ([1], [2], x),
            'hyperu': (1, 2, 3), 'incgam': (2, 3), 'incgamc': (2, 3),
            'lambertw': (x,), 'lerchphi': (x, 2, x), 'lerchzeta': (x, 2, x),
            'lngamma': (x,), 'log': (2,), 'log1p': (x,),
            'polylog': (2, x), 'psi': (x,), 'rootsof1': (3,),
            'sin': (x,), 'sinc': (x,), 'sinh': (x,), 'sqrt': (2,),
            'sqrtn': (2, 3), 'tan': (x,), 'tanh': (x,),
            'weber': (self.pari('I'),), 'zeta': (2,), 'zetahurwitz': (2, x),
        }
        for method, args in cases.items():
            call = getattr(self.pari, method)
            reference = call(*args, precision=256)
            for bits in PRECISIONS:
                with self.subTest(method=method, bits=bits):
                    self.assert_close(call(*args, precision=bits), reference, bits)

    def test_handwritten_vector_calls(self):
        E = self.pari.ellinit([0, -1, 1, -10, -20])
        calls = (
            lambda bits: self.pari(1).eint1(n=3, precision=bits),
            lambda bits: E.ellwp(self.pari('1/3'), flag=1, precision=bits),
        )
        for call in calls:
            reference = call(256)
            for bits in PRECISIONS:
                with self.subTest(call=call, bits=bits):
                    self.assert_close(call(bits), reference, bits)

    def test_number_fields(self):
        polynomial = self.pari('x^3-2')
        reference = polynomial.bnfinit(precision=256).bnf_get_reg()
        for bits in PRECISIONS:
            with self.subTest(bits=bits):
                nf = polynomial.nfinit(precision=bits)
                self.assertEqual(nf.nf_get_sign(), [1, 1])
                embeddings = nf.nfeltembed(self.pari('x'), precision=bits)
                self.assertEqual(len(embeddings), 2)
                for root in embeddings:
                    self.assert_close(polynomial.subst('x', root), self.pari(0), bits)
                bnf = polynomial.bnfinit(precision=bits)
                self.assert_close(bnf.bnf_get_reg(), reference, bits)

    def test_elliptic_curves(self):
        E = self.pari.ellinit([0, -1, 1, -10, -20], precision=256)
        point = self.pari([5, 5])
        reference = E.ellL1(precision=256)
        for bits in PRECISIONS:
            with self.subTest(bits=bits):
                self.assert_close(E.ellL1(precision=bits), reference, bits)
                z = E.ellpointtoz(point, precision=bits)
                self.assert_close(E.ellztopoint(z, precision=bits), point, bits)


if __name__ == '__main__':
    unittest.main()
