"""Shared native thread identity and cysignals support."""

cdef void sig_error_local() noexcept nogil
cdef void *callback_signal_push() except NULL
cdef void callback_signal_pop(void *saved) noexcept
cdef int install_signal_router() except -1
cdef void set_signal_owner_active(bint active) noexcept
cdef bint is_signal_owner() noexcept nogil
