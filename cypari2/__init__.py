from .pari_instance import (Pari, _initialize_pari_owner,
                            _set_owner_request_active)
from .handle_error import PariError
from .gen import Gen, _stabilize_thread_result
from .custom_block import init_custom_block
from .thread_support import _set_signal_owner, _check_request_signal_context
from ._thread_runtime import runtime as _pari_thread_runtime


def _initialize_thread_owner():
    _set_signal_owner()
    _initialize_pari_owner()


init_custom_block()
_pari_thread_runtime.install_initializer(_initialize_thread_owner)
_pari_thread_runtime.install_result_stabilizer(_stabilize_thread_result)
_pari_thread_runtime.install_request_activity_hook(_set_owner_request_active)
_pari_thread_runtime.install_request_guard(_check_request_signal_context)
