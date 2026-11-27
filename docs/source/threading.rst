Calling PARI from Python threads
================================

Create the first ``Pari()`` on the Python main thread. To share its GP session
with Python workers, call ``pari.run_with_threads(application)`` there. It runs
``application`` on a Python thread and uses the main thread to service PARI
calls until the application returns. Join the application's workers before
returning. For example::

    from concurrent.futures import ThreadPoolExecutor
    from cypari2 import Pari

    pari = Pari()

    def application():
        with ThreadPoolExecutor(max_workers=4) as pool:
            return list(pool.map(pari.issquarefree, (15, 16, 17)))

    assert pari.run_with_threads(application) == [1, 0, 1]

A worker can pass and return managed ``Gen`` objects, including values used
after that worker exits. PARI sees one GP session. Its Python calls run
serially and its own native parallel algorithms remain available. A worker
call without an active service raises ``RuntimeError``. Applications which
need the Python main thread for their own event loop must arrange when it
will service PARI.

Batch short operations into a single request with
``pari.run_on_owner(function, *args, **kwargs)``. For example, a Sage worker
can use ``pari.run_on_owner(ZZ(360).euler_phi)``. For downstream Cython code,
submit the entire computation, including allocation, use and release of raw
``GEN`` values and its matching ``sig_on()`` / ``sig_off()`` calls. A client
that owns a clone created on the main thread can cimport
``cypari2.gen.release_clone`` to drop its reference from any Python thread.
New worker calls should begin outside signal-protected frames. Independent
cysignals-protected operations must avoid overlapping across threads because
cysignals shares its jump target across the process.

Callbacks execute on the main thread in the submitting thread's
``contextvars`` context. They can call PARI again. Waiting in a callback for a
worker that needs PARI deadlocks. Fork-based clients can continue to use the
initialized main stack when forking from the idle main thread. Use spawn for
child processes started from workers.
