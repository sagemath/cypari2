from .pari_long cimport pari_longword, pari_ulongword
from .types cimport GEN

cdef void _pari_init_error_handling() noexcept
cdef int _pari_err_handle(GEN E) except 0
cdef void _pari_err_recover(pari_longword errnum) noexcept
