from .paridecl cimport avma

cdef extern from "Python.h" nogil:
    unsigned long PyThread_get_thread_ident() noexcept

cdef unsigned long owner_ident

cdef inline bint is_owner_thread() noexcept nogil:
    return PyThread_get_thread_ident() == owner_ident


cdef void initialize_pari() except *

cdef inline void ensure_pari_initialized() except *:
    if not avma:
        initialize_pari()
