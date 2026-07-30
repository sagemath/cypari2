"""Thread-affine execution support for libpari.

PARI libraries built with ``--enable-tls`` require every thread entering
libpari to own an initialized PARI context.  More importantly, a ``GEN`` on
the PARI stack or clone heap must be managed by the context that created it.

The public cypari2 API therefore uses a single owner thread.  Calls made from
other Python threads are marshalled to that thread.  This module deliberately
does not import any Cython extension module, so it can start before libpari is
initialized and cannot introduce an import cycle.
"""

from __future__ import annotations

import atexit
import functools
import os
import queue
import threading


def _noop():
    return None


def owner_method(method):
    """Decorate an extension method so bound and unbound calls dispatch."""
    @functools.wraps(method)
    def owner_call(*args, **kwargs):
        return runtime.call(method, *args, **kwargs)

    owner_call._cypari2_owner_method = True
    return owner_call


class _Request:
    __slots__ = (
        "callable", "args", "kwargs", "done", "result", "exc_info",
        "stabilize", "activity",
    )

    def __init__(self, callable_, args, kwargs, *, wait=True,
                 stabilize=True, activity=True):
        self.callable = callable_
        self.args = args
        self.kwargs = kwargs
        self.done = threading.Event() if wait else None
        self.result = None
        self.exc_info = None
        self.stabilize = stabilize
        self.activity = activity


class _OwnerIterator:
    """Keep iterator advancement on the PARI owner thread."""

    __slots__ = ("_runtime", "_iterator")

    def __init__(self, runtime, iterator):
        self._runtime = runtime
        self._iterator = iterator

    def __iter__(self):
        return self

    def __next__(self):
        return self._runtime.call(next, self._iterator)


class _PariThreadRuntime:
    """Run all direct libpari access on one long-lived thread."""

    _STOP = object()

    def __init__(self):
        self._start_lock = threading.Lock()
        # Enqueue bookkeeping can decref a temporary Gen and synchronously
        # enter Gen.__dealloc__ on the same Python thread.  Its clone release
        # submits another owner request, so this lock must be re-entrant.
        self._queue_lock = threading.RLock()
        self._queue = queue.SimpleQueue()
        self._thread = None
        self._owner_ident = None
        self._ready = threading.Event()
        self._initializer = None
        self._initialized = False
        self._stabilize = lambda value: value
        self._request_activity = lambda active: None
        self._callback_error_stack = []
        self._forked_with_owner = False
        self._shutting_down = False
        if hasattr(os, "register_at_fork"):
            os.register_at_fork(after_in_child=self._after_fork_child)

    def install_result_stabilizer(self, stabilizer):
        """Install the owner-side hook that detaches results from the stack."""
        self._stabilize = stabilizer

    def install_initializer(self, initializer):
        """Install the function which initializes libpari on the owner."""
        self._initializer = initializer

    def install_request_activity_hook(self, hook):
        """Install the hook used by the asynchronous signal router."""
        self._request_activity = hook

    def is_owner(self):
        """Return whether the current OS thread owns the PARI context."""
        return threading.get_ident() == self._owner_ident

    def ensure_started(self):
        """Start the owner thread, once, before initializing libpari."""
        if self._shutting_down:
            raise RuntimeError("the cypari2 PARI owner thread is shutting down")
        if self._forked_with_owner:
            raise RuntimeError(
                "cypari2 was initialized before fork; use the multiprocessing "
                "'spawn' start method in the child process"
            )
        thread = self._thread
        if thread is None:
            with self._start_lock:
                if self._shutting_down:
                    raise RuntimeError("the cypari2 PARI owner thread is shutting down")
                thread = self._thread
                if thread is None:
                    self._ready.clear()
                    thread = threading.Thread(
                        target=self._run,
                        name="cypari2-pari-owner",
                        daemon=True,
                    )
                    self._thread = thread
                    thread.start()
        self._ready.wait()
        if not thread.is_alive():
            raise RuntimeError("the cypari2 PARI owner thread is no longer available")

    def call(self, callable_, *args, **kwargs):
        """Run ``callable_`` on the owner and return or re-raise its result."""
        if self.is_owner():
            return callable_(*args, **kwargs)
        self.ensure_started()
        request = _Request(callable_, args, kwargs)
        # Serialize the final liveness check and enqueue with shutdown's stop
        # marker.  Otherwise a late request could land behind the marker and
        # wait forever after the owner exits.
        with self._queue_lock:
            if self._shutting_down or not self._thread.is_alive():
                raise RuntimeError("the cypari2 PARI owner thread is no longer available")
            self._queue.put(request)
        request.done.wait()
        if request.exc_info is not None:
            exc, traceback = request.exc_info
            raise exc.with_traceback(traceback)
        return request.result

    def ensure_initialized(self):
        """Ensure that the owner has initialized libpari."""
        if self.is_owner():
            return
        self.call(_noop)

    def submit(self, callable_, *args, **kwargs):
        """Queue best-effort owner work without waiting for it.

        This is used by ``Gen.__dealloc__``.  Failure during interpreter
        shutdown intentionally leaks the clone instead of freeing it from the
        wrong PARI context.
        """
        if self.is_owner():
            callable_(*args, **kwargs)
            return True
        with self._queue_lock:
            if (self._shutting_down or self._thread is None or
                    not self._thread.is_alive()):
                return False
            # Clone release neither returns stack data nor executes a
            # long-running interruptible PARI operation.  Treating every
            # release as a full public request would repeatedly stabilize an
            # already-empty stack and can create a large shutdown backlog.
            self._queue.put(_Request(
                callable_, args, kwargs,
                wait=False, stabilize=False, activity=False,
            ))
        return True

    def call_type_method(self, cls, name, args, kwargs=None):
        """Invoke a special method whose lookup bypasses ``__getattribute__``."""
        if kwargs is None:
            kwargs = {}
        return self.call(getattr(cls, name), *args, **kwargs)

    def protect_iterator(self, iterator):
        """Return an iterator whose advancement is confined to the owner."""
        return _OwnerIterator(self, iterator)

    def enter_python_callback(self):
        """Start tracking PARI evaluator errors in a Python callback."""
        self._callback_error_stack.append(False)

    def note_callback_pari_error(self):
        """Record that PARI reset the evaluator enclosing callbacks."""
        for index in range(len(self._callback_error_stack)):
            self._callback_error_stack[index] = True

    def callback_pari_error_seen(self):
        """Return whether the innermost active callback lost PARI state."""
        return bool(self._callback_error_stack[-1])

    def leave_python_callback(self):
        """Finish callback tracking and return whether PARI reset state."""
        return self._callback_error_stack.pop()

    def _run(self):
        self._owner_ident = threading.get_ident()
        self._ready.set()
        while True:
            request = self._queue.get()
            if request is self._STOP:
                break
            try:
                if request.activity:
                    self._request_activity(True)
                if not self._initialized:
                    if self._initializer is None:
                        raise RuntimeError("cypari2 runtime is not fully initialized")
                    self._initializer()
                    self._initialized = True
                request.result = request.callable(*request.args, **request.kwargs)
            except BaseException as exc:
                # Preserve the original traceback while transferring the
                # exception to the submitting thread.
                request.exc_info = (exc, exc.__traceback__)
            finally:
                if self._initialized and request.stabilize:
                    try:
                        # Also run this after an exception: arbitrary Python
                        # conversion code may have retained a stack Gen by a
                        # side effect even though the request has no result.
                        request.result = self._stabilize(request.result)
                    except BaseException as exc:
                        if request.exc_info is not None:
                            exc.__context__ = request.exc_info[0]
                        request.exc_info = (exc, exc.__traceback__)
                request.callable = None
                request.args = None
                request.kwargs = None
                if request.activity:
                    try:
                        self._request_activity(False)
                    except BaseException as exc:
                        # Never strand a caller if the internal signal hook
                        # itself fails while a request is being torn down.
                        if request.exc_info is None:
                            request.exc_info = (exc, exc.__traceback__)
                if request.done is not None:
                    request.done.set()
        self._owner_ident = None

    def _after_fork_child(self):
        had_owner = self._thread is not None
        try:
            self._request_activity(False)
        except Exception:
            pass
        self._thread = None
        self._owner_ident = None
        self._initialized = False
        self._callback_error_stack = []
        self._queue = queue.SimpleQueue()
        self._start_lock = threading.Lock()
        self._queue_lock = threading.RLock()
        self._ready = threading.Event()
        self._forked_with_owner = had_owner
        self._shutting_down = False

    def shutdown(self):
        """Drain queued work and stop the daemon thread at interpreter exit."""
        if self.is_owner():
            return
        with self._start_lock:
            with self._queue_lock:
                if self._shutting_down:
                    return
                self._shutting_down = True
                thread = self._thread
                if thread is None or not thread.is_alive():
                    return
                self._queue.put(self._STOP)
        # Do not let Python tear extension modules down while a request still
        # executes C code on the owner.  Normal shutdown is immediate because
        # the stop marker follows all already-queued work.
        thread.join()


runtime = _PariThreadRuntime()
atexit.register(runtime.shutdown)
