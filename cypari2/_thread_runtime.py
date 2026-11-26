"""Service Python workers on the application's main PARI stack."""

from concurrent.futures import Future
from contextvars import copy_context
from functools import wraps
from inspect import signature
import os
from queue import Empty, SimpleQueue
import threading

from .thread_support import _is_owner


def owner_method(method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        if _is_owner():
            return method(*args, **kwargs)
        return runtime.call(method, *args, **kwargs)

    wrapped.__signature__ = signature(method)
    del wrapped.__wrapped__
    return wrapped


class _OwnerIterator:
    def __init__(self, iterator):
        self.iterator = iterator

    def __iter__(self):
        return self

    def __next__(self):
        return runtime.call(next, self.iterator)


class _Runtime:
    def __init__(self):
        self.requests = None
        self.lock = threading.RLock()

    def after_fork(self):
        self.requests = None
        self.lock = threading.RLock()

    def call(self, function, /, *args, **kwargs):
        if _is_owner():
            return function(*args, **kwargs)

        result = Future()
        context = copy_context()
        with self.lock:
            if self.requests is None:
                raise RuntimeError("PARI worker calls require run_with_threads() on the main thread")
            self.requests.put((result, context, function, args, kwargs))
        return result.result()

    def call_type_method(self, cls, name, args, kwargs=None):
        return self.call(getattr(cls, name), *args, **(kwargs or {}))

    def call_binary_method(self, cls, name, left, right, *extra):
        if isinstance(left, cls):
            return self.call(getattr(cls, name), left, right, *extra)
        return self.call(getattr(cls, "__r" + name[2:]), right, left, *extra)

    def protect_iterator(self, iterator):
        return _OwnerIterator(iterator)

    def serve(self, function, /, *args, **kwargs):
        from .gen import _stabilize_stack
        from .stack import _check_service_frame

        if not _is_owner() or self.requests is not None:
            raise RuntimeError("run_with_threads() requires the idle main thread")
        _check_service_frame()
        _stabilize_stack()

        requests = SimpleQueue()
        result = Future()

        def driver():
            try:
                result.set_result(function(*args, **kwargs))
            except BaseException as exc:
                result.set_exception(exc)
            finally:
                # Wake the owner as soon as the application exits.
                requests.put(None)

        context = copy_context()
        worker = threading.Thread(target=context.run, args=(driver,), daemon=True)
        with self.lock:
            self.requests = requests
        request = None
        try:
            worker.start()
            while (request := requests.get()) is not None:
                reply, caller_context, target, positional, keywords = request
                try:
                    _check_service_frame()
                    try:
                        value = caller_context.run(target, *positional, **keywords)
                    finally:
                        # Callbacks and exceptions can retain Gens independently
                        # of the return value.
                        _stabilize_stack()
                    reply.set_result(value)
                    del value
                except BaseException as exc:
                    reply.set_exception(exc)
                request = None
                del reply, caller_context, target, positional, keywords
            worker.join()
            return result.result()
        finally:
            with self.lock:
                if self.requests is requests:
                    self.requests = None
            # For example, SIGINT while the main thread is waiting for work.
            if request is not None and not request[0].done():
                request[0].set_exception(RuntimeError("PARI worker service stopped"))
            while True:
                try:
                    request = requests.get_nowait()
                except Empty:
                    break
                if request is not None:
                    request[0].set_exception(RuntimeError("PARI worker service stopped"))


runtime = _Runtime()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=runtime.after_fork)
