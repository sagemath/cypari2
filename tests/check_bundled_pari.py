"""
Check that other projects can compile against the PARI library bundled in a
cypari2 wheel, using the pkg-config file ``pari.pc`` shipped with cypari2.

Run by cibuildwheel on the repaired wheels.
"""

from __future__ import annotations

import ctypes
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pkgconf

import cypari2


def run_pkgconf(*args: str) -> str:
    proc = pkgconf.run_pkgconf(*args, capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def compiler_from_env(var_name: str, fallback: str) -> list[str]:
    value = os.environ.get(var_name)
    if value:
        return shlex.split(value)
    compiler = shutil.which(fallback)
    if compiler is None:
        raise RuntimeError(f"Could not find a compiler for {var_name or fallback}")
    return [compiler]


def compile(compiler: list[str], source: Path, output: Path, flags: list[str]) -> None:
    subprocess.run([*compiler, os.fspath(source), "-o", os.fspath(output), *flags], check=True)


C_PROGRAM = """\
#include <pari/pari.h>

int main(void) {
    pari_init(1000000, 2);
    GEN value = addii(stoi(2), stoi(3));
    int ok = itos(value) == 5;
    pari_close();
    return ok ? 0 : 1;
}
"""

CXX_PROGRAM = """\
extern "C" {
#include <pari/pari.h>
}

int main() {
    pari_init(1000000, 2);
    GEN value = addii(stoi(4), stoi(5));
    int ok = itos(value) == 9;
    pari_close();
    return ok ? 0 : 1;
}
"""

# Does not initialize PARI, but relies on cypari2 having done so. This only
# works if it uses the same libpari as cypari2: another copy of libpari has
# its own uninitialized PARI stack.
C_LIBRARY = """\
#include <pari/pari.h>

long probe_add(long a, long b) {
    pari_sp av = avma;
    long result = itos(addii(stoi(a), stoi(b)));
    set_avma(av);
    return result;
}
"""


def main() -> None:
    package_dir = Path(cypari2.__file__).resolve().parent
    pari_pc = package_dir / "pari.pc"
    if not pari_pc.is_file():
        raise AssertionError(f"Missing pkg-config file: {pari_pc}")

    pkg_config_paths = [Path(path).resolve() for path in pkgconf.get_pkg_config_path()]
    if package_dir not in pkg_config_paths:
        raise AssertionError(f"{package_dir} is not exported via pkgconf entry points")

    cflags = shlex.split(run_pkgconf("--cflags", "pari"))
    libs = shlex.split(run_pkgconf("--libs", "pari"))
    print(f"pari.pc: Cflags: {shlex.join(cflags)}")
    print(f"pari.pc: Libs: {shlex.join(libs)}")

    include_dirs = [Path(flag[2:]).resolve() for flag in cflags if flag.startswith("-I")]
    if package_dir not in include_dirs or not (package_dir / "pari" / "pari.h").is_file():
        raise AssertionError(f"pari.pc does not point to the bundled headers: {cflags}")

    bundled_lib_dirs = [package_dir.parent / "cypari2.libs", package_dir / ".dylibs"]
    library = [Path(flag).resolve() for flag in libs if not flag.startswith("-")]
    if not (
        len(library) == 1
        and library[0].is_file()
        and library[0].parent in bundled_lib_dirs
    ):
        raise AssertionError(f"pari.pc does not point to the bundled library: {libs}")

    flags = [*cflags, *libs]
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        for compiler, program, suffix in [
            (compiler_from_env("CC", "cc"), C_PROGRAM, "c"),
            (compiler_from_env("CXX", "c++"), CXX_PROGRAM, "cc"),
        ]:
            source = tmp / f"probe.{suffix}"
            source.write_text(program)
            executable = tmp / f"probe-{suffix}"
            compile(compiler, source, executable, flags)
            subprocess.run([os.fspath(executable)], check=True)
            print(f"Compiled and ran {source.name} with {compiler[0]}")

        source = tmp / "probe_lib.c"
        source.write_text(C_LIBRARY)
        shared_lib = tmp / "probe_lib.so"
        compile(compiler_from_env("CC", "cc"), source, shared_lib, ["-shared", "-fPIC", *flags])
        probe = ctypes.CDLL(os.fspath(shared_lib))
        probe.probe_add.argtypes = [ctypes.c_long, ctypes.c_long]
        probe.probe_add.restype = ctypes.c_long
        if cypari2.Pari()(2) + 3 != 5 or probe.probe_add(2, 3) != 5:
            raise AssertionError("Library compiled against pari.pc does not work")
        print("Library compiled against pari.pc shares the PARI library with cypari2")

    if sys.platform == "linux":
        maps = Path("/proc/self/maps").read_text().splitlines()
        loaded = {line.split()[-1] for line in maps if "libpari" in line}
        if loaded != {os.fspath(library[0])}:
            raise AssertionError(f"Expected only {library[0]} to be loaded, found {loaded}")


if __name__ == "__main__":
    main()
