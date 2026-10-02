#*****************************************************************************
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
#*****************************************************************************

from cysignals.signals cimport add_custom_signals
from .stack cimport reset_avma

cdef extern from "pari/pari.h":
    int     PARI_SIGINT_block, PARI_SIGINT_pending

cdef extern from *:
    """
    #ifndef _WIN32
    #include <pthread.h>
    static pthread_t cypari2_custom_signal_owner;
    static int cypari2_custom_signal_owner_ready;
    static void cypari2_set_custom_signal_owner(void)
    {
        cypari2_custom_signal_owner = pthread_self();
        cypari2_custom_signal_owner_ready = 1;
    }
    static int cypari2_custom_signal_on_owner(void)
    {
        return cypari2_custom_signal_owner_ready &&
               pthread_equal(pthread_self(), cypari2_custom_signal_owner);
    }
    #else
    #include <windows.h>
    static DWORD cypari2_custom_signal_owner;
    static int cypari2_custom_signal_owner_ready;
    static void cypari2_set_custom_signal_owner(void)
    {
        cypari2_custom_signal_owner = GetCurrentThreadId();
        cypari2_custom_signal_owner_ready = 1;
    }
    static int cypari2_custom_signal_on_owner(void)
    {
        return cypari2_custom_signal_owner_ready &&
               GetCurrentThreadId() == cypari2_custom_signal_owner;
    }
    #endif
    """
    void cypari2_set_custom_signal_owner() noexcept nogil
    int cypari2_custom_signal_on_owner() noexcept nogil


cdef int custom_signal_is_blocked() noexcept:
    if not cypari2_custom_signal_on_owner():
        return 0
    return PARI_SIGINT_block

cdef void custom_signal_unblock() noexcept:
    if not cypari2_custom_signal_on_owner():
        return
    global PARI_SIGINT_block
    PARI_SIGINT_block = 0
    reset_avma()

cdef void custom_set_pending_signal(int sig) noexcept:
    if not cypari2_custom_signal_on_owner():
        return
    global PARI_SIGINT_pending
    PARI_SIGINT_pending = sig

def init_custom_block():
    add_custom_signals(&custom_signal_is_blocked,
                       &custom_signal_unblock,
                       &custom_set_pending_signal)


def _set_custom_signal_owner():
    """Bind PARI-aware cysignals hooks to the permanent owner thread."""
    cypari2_set_custom_signal_owner()
