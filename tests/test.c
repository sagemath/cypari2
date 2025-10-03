// Simple test program using the PARI library
// to compute zeta(2) and factor a polynomial over a finite field, as in the README.
// compile with: gcc -v test.c -o test -I/usr/local/include -L/usr/local/bin -lpari -lgmp

#include <pari/pari.h>

int main() { 
    pari_init(100000000,2);

    // Compute zeta(2)
    GEN z2 = szeta(2, DEFAULTPREC);
    pari_printf("zeta(2) = %Ps\n", z2);

    // p = x^3 + x^2 + x - 1
    GEN gen_3 = stoi(3);
    GEN x = pol_x(0);
    GEN p = gadd(gadd(gadd(gpow(x, gen_3, DEFAULTPREC), gpow(x, gen_2, DEFAULTPREC)), x), gen_m1);
    pari_printf("p = %Ps\n", p);

    // modulus = y^3 + y^2 + y - 1
    GEN y = pol_x(1);
    GEN modulus = gadd(gadd(gadd(gpow(y, gen_3, DEFAULTPREC), gpow(y, gen_2, DEFAULTPREC)), y), gen_m1);
    setvarn(modulus, 1);
    pari_printf("modulus = %Ps\n", modulus);

    // Factor p over F_3[y]/(modulus)
    GEN fq = factorff(p, gen_3, modulus);
    GEN centered = centerlift(lift(fq));
    pari_printf("centerlift(lift(fq)) = %Ps\n", centered);

    pari_close();
    return 0;
}
