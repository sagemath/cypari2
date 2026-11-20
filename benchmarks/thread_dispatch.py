"""Measure the fixed cost of PR #215's PARI owner-thread dispatch.

Run this script with an installed cypari2 build from both ``main`` and this PR,
using the same machine, Python, and PARI. For example, after building each
checkout in its own virtual environment::

    .venv/bin/python benchmarks/thread_dispatch.py

The public ``x + 1`` case is deliberately tiny: on one macOS arm64 machine it
took about 2.4 ms per 10,000 additions on ``main`` and 108-131 ms on this PR
(roughly 45-55 times slower). This is a fixed per-call cost, not slower PARI
arithmetic. An empty owner-thread request alone took about 100 ms per 10,000
calls there; one owner request containing 10,000 additions took about 5 ms.
The larger PARI calculation below helps show how that cost becomes less
significant when each call does substantial work. These numbers are examples,
not performance targets; compare results from the same machine and build.
"""

from timeit import repeat

from cypari2 import Pari

try:
    from cypari2._thread_runtime import runtime
except ModuleNotFoundError as exc:
    if exc.name != "cypari2._thread_runtime":
        raise
    runtime = None  # The main branch has no owner-thread runtime.


pari = Pari()
x = pari(5)


def batched_additions():
    for _ in range(10_000):
        x + 1


def larger_pari_call():
    pari("sum(k=1,100000,k^2)")


def measure(name, operation, number, units_per_call=1):
    duration = min(repeat(operation, number=number, repeat=3))
    units = number * units_per_call
    print(f"{name}: {duration:.6f} s per {units:,} operations "
          f"({duration / units * 1e6:.2f} us/operation)")


# Public API: isolates the overhead of dispatching a cheap PARI operation.
measure("x + 1", lambda: x + 1, 10_000)

# Public API: the same dispatch cost matters much less for substantial work.
measure("larger PARI call", larger_pari_call, 100)

if runtime is not None:
    # Private diagnostics: an empty request measures most of the queue/event
    # round trip. The public batching API shows how much of the x + 1 cost
    # is per-request without exposing raw PARI values to the caller.
    measure("owner no-op", lambda: runtime.call(lambda: None), 10_000)
    measure("owner integer", lambda: runtime.call(lambda: 6), 10_000)
    measure("one batched owner call", lambda: pari.run_on_owner(batched_additions),
            1, units_per_call=10_000)
