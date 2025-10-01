from __future__ import absolute_import

from pathlib import Path

from .generator import PariFunctionGenerator


def rebuild(pari_data: str, force: bool = False, output: None | str = None):
    if output is None:
        output = "cypari2"
    output_dir = Path(output)
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    pari_datadir = Path(pari_data)
    if not pari_datadir.is_dir():
        raise ValueError(f"PARI data directory {pari_datadir} does not exist or is not a directory")

    src_files = [pari_datadir / "pari.desc"] + list(Path("autogen").glob("*.py"))
    gen_files = [
        output_dir / "auto_paridecl.pxd",
        output_dir / "auto_gen.pxi",
    ]

    if not force and all(f.exists() for f in gen_files):
        src_mtime = max(f.stat().st_mtime for f in src_files)
        gen_mtime = min(f.stat().st_mtime for f in gen_files)

        if gen_mtime > src_mtime:
            return

    G = PariFunctionGenerator(pari_datadir, output_dir)
    G()
