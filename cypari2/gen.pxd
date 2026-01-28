cimport cython
from cpython.object cimport PyObject
from cpython.weakref cimport PyWeakref_NewRef, PyWeakref_GetObject
from .types cimport GEN, pari_sp


cdef class Gen_base:
    # The actual PARI GEN
    cdef GEN g


cdef class Gen(Gen_base):
    # There are 3 kinds of memory management for a GEN:
    # * stack: GEN on the PARI stack
    # * clone: refcounted clone on the PARI heap
    # * constant: universal constant such as gen_0
    #
    # A priori, it makes sense to have separate classes for these cases.
    # However, a GEN may be moved from the stack to the heap. This is
    # easier to support when there is just one class. Second, the
    # differences between the cases are really implementation details
    # which should not affect the user.

    # Base address of the GEN that we wrap. On the stack, this is the
    # value of avma when new_gen() was called. For clones, this is the
    # memory allocated by gclone(). For constants, this is NULL.
    cdef GEN address

    cdef inline pari_sp sp(self) noexcept:
        return <pari_sp>self.address

    # Enable weak references in Gen.
    cdef object __weakref__

    # The Gen objects on the PARI stack form a linked list, from the
    # bottom to the top of the stack. This makes sense since we can only
    # deallocate a Gen which is on the bottom of the PARI stack. If this
    # is the last object on the stack, then next = top_of_stack
    # (a singleton object).
    #
    # The connection between the list elements are implemented using the
    # _next attribute. In order to not increase reference counts, the
    # _next attribute is implemented as a weak reference.
    # In the clone and constant cases, this is None.
    #
    # Do not set or access _next directly. Please use the get_next() and
    # set_next() methods.
    cdef object _next

    cdef inline object get_next(self):
        if self._next is None:
            return None
        cdef PyObject* result_ptr = PyWeakref_GetObject(self._next)
        if result_ptr == NULL or <object>result_ptr is None:
            return None
        return <object>result_ptr

    cdef inline void set_next(self, Gen value):
        if value is None:
            self._next = None
        else:
            self._next = PyWeakref_NewRef(value, None)

    # A cache for __getitem__. Initially, this is None but it will be
    # turned into a dict when needed.
    cdef dict itemcache

    cdef inline int cache(self, key, value) except -1:
        """
        Add ``(key, value)`` to ``self.itemcache``.
        """
        if self.itemcache is None:
            self.itemcache = {}
        self.itemcache[key] = value

    cdef Gen new_ref(self, GEN g)

    cdef GEN fixGEN(self) except NULL

    cdef GEN ref_target(self) except NULL


cdef inline Gen Gen_new(GEN g, GEN addr):
    z = <Gen>Gen.__new__(Gen)
    z.g = g
    z.address = addr
    return z


cdef Gen list_of_Gens_to_Gen(list s)
cpdef Gen objtogen(s)
