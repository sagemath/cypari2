"""
Memory management for Gens on the PARI stack or the heap
********************************************************
"""

# ****************************************************************************
#       Copyright (C) 2016 Luca De Feo <luca.defeo@polytechnique.edu>
#       Copyright (C) 2018 Jeroen Demeyer <J.Demeyer@UGent.be>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

cimport cython

from cpython.ref cimport PyObject, _Py_REFCNT
from cpython.exc cimport PyErr_SetString

from cysignals.signals cimport (sig_on, sig_off, sig_block, sig_unblock,
                                sig_error)

from .gen cimport Gen, Gen_new
from .paridecl cimport (avma, pari_mainstack, gnil, gcopy,
                        is_universal_constant, is_on_stack,
                        isclone, gclone, gclone_refc,
                        paristack_setsize)

from warnings import warn


cdef extern from *:
    int sig_on_count "cysigs.sig_on_count"
    int block_sigint "cysigs.block_sigint"


# Singleton object to denote the top of the PARI stack
cdef Gen top_of_stack = Gen_new(gnil, NULL)

# Pointer to the Gen on the bottom of the PARI stack.
cdef PyObject* stackbottom = <PyObject*>top_of_stack


cdef void remove_from_pari_stack(Gen self) noexcept:
    global avma, stackbottom
    if <PyObject*>self is not stackbottom:
        print("ERROR: removing wrong instance of Gen")
        print(f"Expected: {<object>stackbottom}")
        print(f"Actual:   {self}")
    if sig_on_count and not block_sigint:
        PyErr_SetString(SystemError, "calling remove_from_pari_stack() inside sig_on()")
        sig_error()
    if self.sp() != avma:
        if avma > self.sp():
            print("ERROR: inconsistent avma when removing Gen from PARI stack")
            print(f"Expected: 0x{self.sp():x}")
            print(f"Actual:   0x{avma:x}")
        else:
            reset_avma()
    n = self.get_next()
    stackbottom = <PyObject*>n
    self.set_next(None)
    reset_avma()


cdef inline Gen Gen_stack_new(GEN x):
    global stackbottom
    n = <Gen>stackbottom
    z = Gen_new(x, <GEN>avma)
    z.set_next(n)
    stackbottom = <PyObject*>z
    sz = z.sp()
    sn = n.sp()
    if sz > sn:
        raise SystemError(f"objects on PARI stack in invalid order (first: 0x{sz:x}; next: 0x{sn:x})")
    return z


cdef void reset_avma() noexcept:
    global avma
    avma = (<Gen>stackbottom).sp()


cdef void clear_stack() noexcept:
    sig_off()
    reset_avma()


cdef int move_gens_to_heap(pari_sp lim) except -1:
    while avma < lim and stackbottom is not <PyObject*>top_of_stack:
        current = <Gen>stackbottom
        sig_on()
        current.g = gclone(current.g)
        current.itemcache = None
        sig_block()
        remove_from_pari_stack(current)
        sig_unblock()
        sig_off()
        current.address = current.g


cdef int before_resize() except -1:
    move_gens_to_heap(-1)
    if top_of_stack.sp() != pari_mainstack.top:
        raise RuntimeError("cannot resize PARI stack here")


cdef int set_pari_stack_size(size_t size, size_t sizemax) except -1:
    before_resize()
    sig_on()
    paristack_setsize(size, sizemax)
    sig_off()
    after_resize()


cdef void after_resize() noexcept:
    top_of_stack.address = <GEN>pari_mainstack.top


cdef Gen new_gen(GEN x):
    sig_off()
    if x is gnil:
        reset_avma()
        return None
    return new_gen_noclear(x)


cdef new_gens2(GEN x, GEN y):
    sig_off()
    global avma
    av = avma
    g1 = new_gen_noclear(x)
    avma = av
    g2 = new_gen_noclear(y)
    return (g1, g2)


cdef Gen new_gen_noclear(GEN x):
    if not is_on_stack(x):
        reset_avma()
        if is_universal_constant(x):
            return Gen_new(x, NULL)
        elif isclone(x):
            gclone_refc(x)
            return Gen_new(x, x)
        raise SystemError("new_gen() argument not on PARI stack, not on PARI heap and not a universal constant")
    z = Gen_stack_new(x)
    if (pari_mainstack.top - avma) >= pari_mainstack.size // 2:
        if sig_on_count == 0:
            try:
                move_gens_to_heap(-1)
            except MemoryError:
                pass
    return z


cdef Gen clone_gen(GEN x):
    x = gclone(x)
    clear_stack()
    return Gen_new(x, x)


cdef Gen clone_gen_noclear(GEN x):
    x = gclone(x)
    return Gen_new(x, x)


@cython.no_gc
cdef class DetachGen:
    def __init__(self, s):
        self.source = s

    cdef GEN detach(self) except NULL:
        src = <Gen?>self.source
        self.source = None
        cdef GEN res = src.g
        if is_on_stack(res):
            if _Py_REFCNT(<PyObject*>src) != 1:
                raise SystemError("cannot detach a Gen which is still referenced")
        elif is_universal_constant(res):
            pass
        else:
            res = gcopy(res)
        global avma
        cdef pari_sp av = avma
        avma = src.sp()
        del src
        avma = av
        return res
