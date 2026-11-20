"""Check the installed package and the origin of the loaded PARI library."""

import argparse
import ctypes
import json
import os
from pathlib import Path
import platform
import sys

import cypari2


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--bundled", action="store_true", help="require PARI from the installed wheel")
args = parser.parse_args()
prefix = Path(sys.prefix).resolve() if args.bundled else Path(os.environ["PARI_PREFIX"]).resolve()
module = Path(cypari2.__file__).resolve()
if sys.prefix == sys.base_prefix or not module.is_relative_to(Path(sys.prefix).resolve()):
    raise SystemExit(f"cypari2 is not installed in the fresh venv: {module}")
pari = cypari2.Pari()
version = tuple(int(component) for component in pari.version())
if version[:3] != (2, 19, 1):
    raise SystemExit(f"Unexpected PARI runtime version: {version}")
if platform.system() == "Linux":
    libraries = {
        Path(line.split()[-1]).resolve()
        for line in Path("/proc/self/maps").read_text().splitlines()
        if "/libpari" in line
    }
else:
    dyld = ctypes.CDLL(None)
    dyld._dyld_image_count.restype = ctypes.c_uint32
    dyld._dyld_get_image_name.argtypes = [ctypes.c_uint32]
    dyld._dyld_get_image_name.restype = ctypes.c_char_p
    libraries = {
        Path(name.decode()).resolve()
        for index in range(dyld._dyld_image_count())
        if (name := dyld._dyld_get_image_name(index)) and b"/libpari" in name
    }
if not libraries or any(not path.is_relative_to(prefix) for path in libraries):
    raise SystemExit(f"Unexpected loaded PARI libraries: {libraries}")
print(json.dumps({"mode": "bundled" if args.bundled else "prefix",
                  "python": sys.version, "module": str(module),
                  "pari_version": version, "pari_libraries": sorted(map(str, libraries))}, indent=2))
