from .types cimport GEN, pari_sp
from .gen cimport Gen_base, Gen


cdef Gen new_gen(GEN x)
cdef new_gens2(GEN x, GEN y)
cdef Gen new_gen_noclear(GEN x)
cdef Gen clone_gen(GEN x)
cdef Gen clone_gen_noclear(GEN x)

cdef void clear_stack()
cdef void reset_avma()

cdef void remove_from_pari_stack(Gen self)
cdef int move_gens_to_heap(pari_sp lim) except -1


cdef class DetachGen:
    cdef source

    cdef GEN detach(self) except NULL
