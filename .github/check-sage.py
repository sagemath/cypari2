"""Exercise Sage's compiled PARI conversions with the installed candidate."""

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
