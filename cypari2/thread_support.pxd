"""Low-level helpers for the single PARI owner thread."""

from cysignals.signals cimport cysigs


cdef extern from *:
    """
    #include <signal.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "struct_signals.h"

    #ifndef _WIN32
    #include <pthread.h>

    static pthread_t cypari2_signal_owner;
    static cysigs_t *cypari2_signal_state;
    static volatile sig_atomic_t cypari2_signal_owner_ready;
    static volatile sig_atomic_t cypari2_signal_owner_active;
    static volatile sig_atomic_t cypari2_signal_router_ready;
    static const int cypari2_routed_signals[] = { SIGINT, SIGALRM, SIGHUP };
    static struct sigaction cypari2_original_actions[3];

    static void
    cypari2_call_original_signal_handler(int index, int sig,
                                         siginfo_t *info, void *context)
    {
        struct sigaction *action = &cypari2_original_actions[index];
        if (action->sa_handler == SIG_IGN)
            return;
        if (action->sa_handler == SIG_DFL)
        {
            signal(sig, SIG_DFL);
            raise(sig);
            return;
        }
        if (action->sa_flags & SA_SIGINFO)
            action->sa_sigaction(sig, info, context);
        else
            action->sa_handler(sig);
    }

    static void
    cypari2_signal_router(int sig, siginfo_t *info, void *context)
    {
        int index;
        for (index = 0; index < 3; index++)
            if (cypari2_routed_signals[index] == sig)
                break;
        if (index == 3)
            return;

        if (cypari2_signal_owner_ready && cypari2_signal_owner_active &&
            cypari2_signal_state != NULL &&
            cypari2_signal_state->sig_on_count > 0 &&
            !pthread_equal(pthread_self(), cypari2_signal_owner))
        {
            pthread_kill(cypari2_signal_owner, sig);
            return;
        }
        cypari2_call_original_signal_handler(index, sig, info, context);
    }

    static int
    cypari2_install_signal_router(void *opaque)
    {
        struct sigaction action;
        int i;
        cypari2_signal_owner = pthread_self();
        cypari2_signal_state = (cysigs_t *)opaque;
        cypari2_signal_owner_ready = 1;
        if (cypari2_signal_router_ready)
            return 0;

        for (i = 0; i < 3; i++)
            if (sigaction(cypari2_routed_signals[i], NULL,
                          &cypari2_original_actions[i]) < 0)
                return -1;
        for (i = 0; i < 3; i++)
        {
            action = cypari2_original_actions[i];
            action.sa_sigaction = cypari2_signal_router;
            action.sa_flags |= SA_SIGINFO;
            if (sigaction(cypari2_routed_signals[i], &action, NULL) < 0)
            {
                while (i-- > 0)
                    sigaction(cypari2_routed_signals[i],
                              &cypari2_original_actions[i], NULL);
                return -1;
            }
        }
        cypari2_signal_router_ready = 1;
        return 0;
    }

    static void
    cypari2_set_signal_owner_active(int active)
    {
        cypari2_signal_owner_active = !!active;
    }

    static int
    cypari2_is_signal_owner(void)
    {
        return !cypari2_signal_owner_ready ||
               pthread_equal(pthread_self(), cypari2_signal_owner);
    }
    #else
    #include <windows.h>
    static DWORD cypari2_signal_owner;
    static int cypari2_signal_owner_ready;
    static int cypari2_install_signal_router(void *opaque)
    {
        (void)opaque;
        cypari2_signal_owner = GetCurrentThreadId();
        cypari2_signal_owner_ready = 1;
        return 0;
    }
    static void cypari2_set_signal_owner_active(int active)
    { (void)active; }
    static int cypari2_is_signal_owner(void)
    {
        return !cypari2_signal_owner_ready ||
               GetCurrentThreadId() == cypari2_signal_owner;
    }
    #endif

    typedef struct
    {
        cyjmp_buf env;
        int sig_on_count;
        int block_sigint;
        const char *message;
    } cypari2_callback_signal_frame;

    static void
    cypari2_sig_error_current_thread(void *opaque)
    {
        cysigs_t *state = (cysigs_t *)opaque;
        if (state->sig_on_count <= 0)
        {
            fprintf(stderr, "sig_error_local() without sig_on()\\n");
            raise(SIGABRT);
            return;
        }
        cylongjmp(state->env, SIGABRT);
    }

    static void *
    cypari2_callback_signal_push(void *opaque)
    {
        cysigs_t *state = (cysigs_t *)opaque;
        cypari2_callback_signal_frame *frame =
            (cypari2_callback_signal_frame *)malloc(sizeof(*frame));
        if (frame == NULL)
            return NULL;
        memcpy(frame->env, state->env, sizeof(frame->env));
        frame->sig_on_count = state->sig_on_count;
        frame->block_sigint = state->block_sigint;
        frame->message = state->s;

        /* A PARI call made by the Python callback must establish its own
         * jump target.  Otherwise nested sig_on() merely increments the
         * outer counter and an error jumps across live Python frames. */
        state->sig_on_count = 0;
        /* call_python() blocks interrupts around arbitrary Python code.  A
         * deliberate nested PARI call needs a complete inner signal frame,
         * though, otherwise SIGINT/SIGALRM remain deferred forever while the
         * nested computation runs.  With count == 0, signals received by
         * ordinary Python code are still recorded rather than long-jumping. */
        state->block_sigint = 0;
        return frame;
    }

    static void
    cypari2_callback_signal_pop(void *opaque, void *saved)
    {
        cysigs_t *state = (cysigs_t *)opaque;
        cypari2_callback_signal_frame *frame =
            (cypari2_callback_signal_frame *)saved;
        if (frame == NULL)
            return;
        memcpy(state->env, frame->env, sizeof(frame->env));
        state->sig_on_count = frame->sig_on_count;
        state->block_sigint = frame->block_sigint;
        state->s = frame->message;
        free(frame);
    }
    """
    void cypari2_sig_error_current_thread(void *state) noexcept nogil
    void *cypari2_callback_signal_push(void *state) noexcept nogil
    void cypari2_callback_signal_pop(void *state, void *saved) noexcept nogil
    int cypari2_install_signal_router(void *state) noexcept nogil
    void cypari2_set_signal_owner_active(int active) noexcept nogil
    int cypari2_is_signal_owner() noexcept nogil


cdef inline void sig_error_local() noexcept nogil:
    """Jump to this thread's active ``sig_on`` without a process signal."""
    cypari2_sig_error_current_thread(<void *>&cysigs)


cdef inline void *callback_signal_push() except NULL:
    """Allow PARI calls in a Python callback to use a nested jump target."""
    cdef void *saved = cypari2_callback_signal_push(<void *>&cysigs)
    if saved is NULL:
        raise MemoryError
    return saved


cdef inline void callback_signal_pop(void *saved) noexcept:
    """Restore the PARI caller's cysignals jump target."""
    cypari2_callback_signal_pop(<void *>&cysigs, saved)


cdef inline int install_signal_router() except -1:
    """Route asynchronous cysignals interrupts to the PARI owner."""
    if cypari2_install_signal_router(<void *>&cysigs) < 0:
        raise OSError("failed to install cypari2 signal router")
    return 0


cdef inline void set_signal_owner_active(bint active) noexcept:
    cypari2_set_signal_owner_active(active)


cdef inline bint is_signal_owner() noexcept nogil:
    return cypari2_is_signal_owner()
