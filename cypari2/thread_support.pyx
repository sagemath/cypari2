"""Identify the thread on which cysignals and the main PARI stack belong."""

import os
import threading

owner_ident = threading.main_thread().ident


cdef void initialize_pari() except *:
    from cypari2 import Pari
    Pari()


def _is_owner():
    return is_owner_thread()


def _after_fork():
    global owner_ident
    if not is_owner_thread():
        # The parent main thread's PARI TLS did not survive this fork.
        owner_ident = 0


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork)
