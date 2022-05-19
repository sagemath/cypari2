from .types cimport *

cdef class PariThreadPool:
    cdef size_t nbthreads
    cdef pari_thread * pths
    cdef size_t ithread
