r"""
Multithreading from Python
**************************
"""

#*****************************************************************************
#       Copyright (C) 2022 Vincent Delecroix <vincent.delecroix@labri.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from libc.stdlib cimport malloc, calloc, free

from .types cimport *
from .paridecl cimport *
from gen cimport Gen, objtogen

cdef class PariThreadPool:
    r"""
    Pari thread allocator

    This class is intended to be used in conjunction with the multithreading
    capabilities of the ``ThreadPoolExecutor`` from the ``concurrent.futures``
    Python library.

    Examples:

    >>> from concurrent.futures import ThreadPoolExecutor, as_completed
    >>> from cypari2 import Pari, PariThreadPool
    >>> pari = Pari()
    >>> pari.default('nbthreads', 1)
    >>> max_workers = 4
    >>> pari_pool = PariThreadPool(max_workers)
    >>> square_free = []
    >>> with ThreadPoolExecutor(max_workers=max_workers, initializer=pari_pool.initializer) as executor:
    ...     futures = {executor.submit(pari.issquarefree, n): n for n in range(10**6, 10**6 + 1000)}
    ...     for future in as_completed(futures):
    ...         n = futures[future]
    ...         if future.result():
    ...             square_free.append(n)
    >>> square_free.sort()
    >>> square_free
    [1000001, 1000002, 1000003, 1000005, 1000006, ..., 1000994, 1000995, 1000997, 1000999]
    """
    def __init__(self, size_t nbthreads, size_t size=8000000, size_t sizemax=0):
        r"""
        INPUT:

        - ``nbthreads`` -- the number of threads to allocate

        - ``size`` -- (default: 8000000) the number of bytes for the
          initial PARI stack (see notes below)

        - ``sizemax`` -- (default: 0) the maximal number of bytes for the
          dynamically increasing PARI stack.
        """
        cdef size_t i
        size = max(size, pari_mainstack.rsize)
        sizemax = max(max(size, pari_mainstack.vsize), sizemax)
        self.pths = <pari_thread *> calloc(nbthreads, sizeof(pari_thread))
        for i in range(nbthreads):
            pari_thread_valloc(self.pths + i, size, sizemax, NULL)
        self.ithread = 0
        self.nbthreads = nbthreads

    def __dealloc__(self):
        cdef size_t i
        for i in range(self.ithread):
            pari_thread_free(self.pths + i)
        free(self.pths)

    def __repr__(self):
        return 'Pari thread pool with {} threads'.format(self.nbthreads)

    def initializer(self):
        if self.ithread >= self.nbthreads:
            raise ValueError('no more thread available')
        pari_thread_start(self.pths + self.ithread)
        self.ithread += 1
