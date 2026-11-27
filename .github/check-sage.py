"""Exercise Sage's compiled PARI conversions with the installed candidate."""

from concurrent.futures import ThreadPoolExecutor
import os
import sys
from pathlib import Path

import cypari2

venv = Path(sys.prefix).resolve()
assert Path(cypari2.__file__).resolve().is_relative_to(venv), cypari2.__file__

from sage.all import QQ, ZZ, pari
from sage.libs.pari import convert_sage

assert Path(convert_sage.__file__).resolve().is_relative_to(venv), convert_sage.__file__
integer = ZZ(2) ** 130 + 1
rational = QQ(integer) / 7
for value in (integer, rational):
    converted = pari(value)
    assert isinstance(converted, cypari2.Gen)
    assert convert_sage.gen_to_sage(converted) == value

assert ZZ(360).euler_phi() == 96


def threaded_sage():
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert pool.submit(pari.issquarefree, ZZ(15)).result() == 1
        assert pool.submit(pari.run_on_owner, ZZ(360).euler_phi).result() == 96
        converted = pool.submit(pari, rational).result()
        assert pari.run_on_owner(convert_sage.gen_to_sage, converted) == rational


# A manual run can select a source revision from before the worker API.
# PR and tag builds must exercise it.
if not os.environ.get("CYPARI2_TEST_SOURCE_REF") or hasattr(pari, "run_with_threads"):
    pari.run_with_threads(threaded_sage)
