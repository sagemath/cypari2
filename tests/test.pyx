# Simple test program using the PARI library in Cython
# to compute zeta(2) and factor a polynomial over a finite field, as in the README.

from cypari2.paridecl cimport pari_printf, pari_init, pari_close, DEFAULTPREC, szeta, stoi, pol_x, gpow, gadd, factorff, lift, centerlift, setvarn, gen_2, gen_m1, gen_0, INIT_DFTm, pari_init_opts, pari_mainstack
from cypari2.types cimport GEN
from cypari2.closure cimport _pari_init_closure
from cypari2.stack cimport (new_gen, new_gen_noclear, clear_stack,
                     set_pari_stack_size, before_resize, after_resize)
from libc.stdio cimport printf

def main():

    pari_init(100000000, 2)

    # Compute zeta(2)
    cdef GEN z2 = szeta(2, DEFAULTPREC)
    pari_printf(b"zeta(2) = %Ps\n", z2)

    # p = x^3 + x^2 + x - 1
    cdef GEN gen_3 = stoi(3)
    cdef GEN x = pol_x(0)
    cdef GEN p = gadd(gadd(gadd(gpow(x, gen_3, DEFAULTPREC), gpow(x, gen_2, DEFAULTPREC)), x), gen_m1)
    pari_printf(b"p = %Ps\n", p)

    # modulus = y^3 + y^2 + y - 1
    cdef GEN y = pol_x(1)
    cdef GEN modulus = gadd(gadd(gadd(gpow(y, gen_3, DEFAULTPREC), gpow(y, gen_2, DEFAULTPREC)), y), gen_m1)
    setvarn(modulus, 1)
    pari_printf(b"modulus = %Ps\n", modulus)

    # Factor p over F_3[y]/(modulus)
    cdef GEN fq = factorff(p, gen_3, modulus)
    cdef GEN centered = centerlift(lift(fq))
    pari_printf(b"centerlift(lift(fq)) = %Ps\n", centered)

    pari_close()
