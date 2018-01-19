from .types cimport *


cdef class Gen_base:
    # The actual PARI GEN
    cdef GEN g


cdef class Gen(Gen_base):
    # Chunk of memory containing g, typically allocated in
    # deepcopy_to_python_heap(). This can be NULL if there was no memory
    # allocated.
    cdef void* chunk

    # Parent Gen: this is usually None, but it can be used when this
    # Gen is a part of some other Gen. In that case, chunk will be NULL
    # because the parent has allocated the memory.
    cdef Gen_base parent

    # A cache for __getitem__. Initially, this is None but it will be
    # turned into a dict when needed. This is not just an optional
    # cache, but it is required to implement __setitem__ correctly:
    # __setitem__ will set an entry of one Gen to another Gen. To
    # prevent Python from garbage collecting the other Gen, we must put
    # it in itemcache.
    cdef dict itemcache

    cdef inline int cache(self, key, value) except -1:
        """
        Add ``(key, value)`` to ``self.itemcache``.
        """
        if self.itemcache is None:
            self.itemcache = {}
        self.itemcache[key] = value

    cdef new_ref(self, GEN g)


cdef Gen list_of_Gens_to_Gen(list s)
cpdef Gen objtogen(s)
