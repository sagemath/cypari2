Threading model
===============

The Python API can be called from arbitrary Python threads.  CyPari2 sends
every operation which touches libpari to one long-lived owner thread.  This
includes construction of :class:`~cypari2.gen.Gen` objects, methods on
:class:`~cypari2.pari_instance.Pari` and :class:`~cypari2.gen.Gen`, conversion,
error recovery, and destruction of cloned ``GEN`` values.  Calls from several
Python threads are therefore safe but are serialized.

A ``Gen`` returned on one Python thread may be retained, used, and destroyed
on another thread.  Before a result leaves the owner, CyPari2 moves every
contained ``Gen`` from the PARI stack to the owner context's clone heap.
The same cleanup runs after exceptions and covers ``Gen`` objects retained by
side effects in Python conversion hooks or callbacks.

PARI also provides ``pari_thread_start`` and a private stack for each native
thread.  That model requires a parent to copy a result out of the child stack
before freeing it.  It does not by itself fit a Python ``Gen``, whose lifetime,
aliases, and eventual destruction thread are arbitrary.  Keeping one
long-lived owner gives every wrapped ``GEN`` one stable allocation and clone
registry instead of attempting to migrate an object graph between transient
caller stacks.

PARI's own internal pthread parallelism remains available.  For example, a
parallel PARI operation using a native GP closure can still use the configured
``nbthreads`` value.  A Python callable cannot execute inside a PARI worker,
because those workers do not own the Python GIL.  Such an attempt raises a
``PariError`` instead of entering Python from the foreign thread.  Set
``nbthreads`` to 1 when a PARI parallel API must invoke a Python callable::

    pari.default("nbthreads", 1)
    pari.parapply(lambda value: value + 1, range(4))

Python callbacks which run on the owner may call CyPari2 again.  Successful
results and uncaught nested PARI exceptions are propagated normally.  PARI
resets its evaluator when reporting an error, so a callback cannot catch a
nested :class:`~cypari2.handle_error.PariError` and continue its enclosing PARI
evaluation.  CyPari2 detects that case and aborts the outer evaluation with a
:class:`RuntimeError` instead of returning into the reset evaluator.
The callback runs with the owner's Python thread-local state and a snapshot
of the submitting thread's :mod:`contextvars` context.  It must not
synchronously wait for another thread to finish a CyPari2 call, since that
call is queued behind the callback itself; make a nested CyPari2 call directly
in the callback instead.  Output emitted by a native PARI worker is written
directly to the process's C ``stdout``; redirecting :data:`sys.stdout` only
affects output emitted on the owner.  Other owner-only hooks, including stack
resizing and IPython plotting, raise ``PariError`` when invoked by a native
PARI worker.  On POSIX, asynchronous cysignals interrupts such as ``SIGINT``
and ``SIGALRM`` are routed to the owner while it is inside a request, then
re-raised in the calling Python thread.

Cython integration
------------------

The deprecated Cython conversion helpers ``new_gen_from_double`` and
``new_t_COMPLEX_from_double`` also dispatch to the owner and return stable
``Gen`` objects.  Other Cython code that reads or creates raw ``GEN`` values
must run its whole PARI computation on the owner.  Use
:meth:`~cypari2.pari_instance.Pari.run_on_owner` as the entry point::

    # compute_in_cython is a Python-callable Cython function. Its PARI stack
    # allocations and sig_on()/sig_off() region all execute on the owner.
    result = pari.run_on_owner(compute_in_cython, argument)

Return Python values or managed ``Gen`` objects from that function, never
raw stack pointers.  Direct access to raw ``GEN`` values on the submitting
thread is not supported: constructing ``Pari()`` no longer initializes that
thread's PARI stack.  Existing Cython consumers must migrate such operations
to the owner entry point.

The cysignals jump state is shared between threads.  A caller must leave its
own ``sig_on()`` region before waiting for an owner request; the request raises
``RuntimeError`` if it finds an existing foreign signal frame.  Move the
entire protected computation into ``run_on_owner`` instead.  External Cython
code must also avoid running an independent cysignals-protected operation
concurrently with the owner.  Routing a signal cannot make it safe to jump
between two threads' C stacks.

``run_on_owner`` can also batch several Python API operations into one
request, reducing the cost of thread dispatch.  The same callback rules
apply: the callable must not wait for another thread to make a CyPari2 call.

Process lifecycle
-----------------

Forking a process after CyPari2 has initialized libpari cannot preserve the
vanished owner thread or its PARI context.  A child in that state raises
``RuntimeError`` on use.  With :mod:`multiprocessing`, use the ``spawn`` start
method, or fork before the first CyPari2 operation, including module-level
conversion helpers.

This guarantee covers the public Python API, including direct unbound method
calls on the extension types.  The Cython integration requirements above
also apply to libraries embedding those calls inside their own signal frames.
