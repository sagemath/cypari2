from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

import cypari2
import pkgconf


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


def compile_and_run(compiler: list[str], source_path: Path, output_path: Path, flags: list[str]) -> None:
    subprocess.run(
        [*compiler, os.fspath(source_path), "-o", os.fspath(output_path), *flags],
        check=True,
    )
    subprocess.run([os.fspath(output_path)], check=True)


def main() -> None:
    package_dir = Path(cypari2.__file__).resolve().parent
    pari_pc = package_dir / "pari.pc"
    if not pari_pc.is_file():
        raise AssertionError(f"Missing bundled pkg-config file: {pari_pc}")

    pkg_config_paths = [Path(path).resolve() for path in pkgconf.get_pkg_config_path()]
    if package_dir.resolve() not in pkg_config_paths:
        raise AssertionError(f"{package_dir} is not exported via pkgconf entry points")

    flags = shlex.split(run_pkgconf("--cflags", "--libs", "pari"))
    include_dirs = [Path(flag[2:]).resolve() for flag in flags if flag.startswith("-I")]
    lib_dirs = [Path(flag[2:]).resolve() for flag in flags if flag.startswith("-L")]

    if package_dir.resolve() not in include_dirs:
        raise AssertionError(f"pkg-config did not resolve wheel-local headers: {include_dirs}")

    expected_lib_dirs = [
        (package_dir.parent / "cypari2.libs").resolve(),
        (package_dir / ".dylibs").resolve(),
    ]
    if not any(path in lib_dirs for path in expected_lib_dirs):
        raise AssertionError(f"pkg-config did not resolve wheel-local libraries: {lib_dirs}")

    c_source = """\
#include <pari/pari.h>

int main(void) {
    pari_init(1000000, 2);
    GEN value = addii(stoi(2), stoi(3));
    int ok = itos(value) == 5;
    pari_close();
    return ok ? 0 : 1;
}
"""
    cxx_source = """\
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

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_path = tmpdir_path / "probe.c"
        cxx_path = tmpdir_path / "probe.cc"
        c_path.write_text(c_source)
        cxx_path.write_text(cxx_source)

        compile_and_run(compiler_from_env("CC", "cc"), c_path, tmpdir_path / "probe-c", flags)
        compile_and_run(compiler_from_env("CXX", "c++"), cxx_path, tmpdir_path / "probe-cxx", flags)


if __name__ == "__main__":
    main()
