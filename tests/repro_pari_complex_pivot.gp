\\ Manual reproducer for the complex numerical pivot failure.
\\ Run: gp -fq tests/repro_pari_complex_pivot.gp
\\
\\ Verified locally with unpatched PARI 2.17.4 and 2.19.0:
\\   error("impossible inverse in divrr: 0.E-32.")
\\ With the candidate Gaussian pivot fix applied to PARI 2.19.0,
\\ this returns eigenvalues approximately +/-sqrt(2)*I and eigenvectors.
\\
\\ This constructs the same values and precisions as the cypari2 call
\\   pari.matrix(2, 2, [0., 1., -2., 0.]).mateigen(flag=1, precision=64)
\\ Python's floating-point zero is converted to a PARI zero with
\\ binary exponent -53. GP's 0. at this working precision has exponent
\\ -64, so multiplication by 2^11 produces the corresponding zero.

repro() = {
  localbitprec(64);
  my(z = 0. * 2^11);
  mateigen([z, 1.; -2., z], 1)
};
iferr(print(repro()), E, print(E));
quit
