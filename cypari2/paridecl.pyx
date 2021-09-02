"""
Expose ``PARI_SIGINT_block`` and ``PARI_SIGINT_pending`` for runtime use of ``cysignals``.

AUTHORS:

- Jonathan Kliem (2021-09-02)
"""
#*****************************************************************************
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

def _PARI_SIGINT_block_pt():
    """
    Return the address of ``PARI_SIGINT_block``.

        .. WARNING::

        Changing this variable will change PARI's signal handling.
    """
    return <size_t> &PARI_SIGINT_block

def _PARI_SIGINT_pending_pt():
    """
    Return the address of ``PARI_SIGINT_pending``.

        .. WARNING::

        Changing this variable will change PARI's signal handling.
    """
    return <size_t> &PARI_SIGINT_pending
