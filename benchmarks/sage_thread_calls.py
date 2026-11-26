"""Compare paired cypari2/Sage builds with the same Python, libpari and host.

Run with the Python of each installed environment. Durations are medians of
seven repeats, in microseconds per operation. Use a source build against the
same libpari as Sage for each cypari2 version.
"""

from importlib.metadata import version
from statistics import median
from timeit import repeat

from sage.all import GF, ZZ, pari


def measure(name, calculation, count):
    seconds = median(repeat(calculation, number=count, repeat=7))
    print(f"{name:32s} {seconds * 1e6 / count:10.3f} us", flush=True)


def main():
    number = ZZ(360)
    x = pari(5)
    dedicated = hasattr(pari, "run_on_owner") and not hasattr(pari, "run_with_threads")
    print(f"Sage {version('sagemath')}, cypari2 {version('cypari2')}, PARI {pari.version()}")
    measure("Gen addition", lambda: x + 1, 10_000)
    measure("issquarefree", lambda: pari.issquarefree(15), 10_000)
    measure("GP sum", lambda: pari("sum(k=1,100000,k^2)"), 25)

    def on_stack():
        measure("Sage euler_phi", lambda: number.euler_phi(), 20_000)
        a = GF(25, "a", impl="pari_ffelt").gen()
        measure("PARI finite-field product", lambda: a * a, 20_000)

    if dedicated:
        measure("euler_phi per request", lambda: pari.run_on_owner(number.euler_phi), 10_000)
        pari.run_on_owner(on_stack)
    else:
        on_stack()

    if hasattr(pari, "run_with_threads"):
        def application():
            measure("euler_phi per request", lambda: pari.run_on_owner(number.euler_phi), 5000)
            pari.run_on_owner(lambda: measure("batched euler_phi", number.euler_phi, 20_000))
        pari.run_with_threads(application)


if __name__ == "__main__":
    main()
