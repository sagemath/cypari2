from __future__ import absolute_import

import glob
from os.path import exists, getmtime, join
from pathlib import Path

from .generator import PariFunctionGenerator
from .paths import pari_share


def rebuild(force: bool = False, output: None | str = None):
    if output is None:
        output = "cypari2"
    output_dir = Path(output)
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    src_files = [join(pari_share(), "pari.desc")] + glob.glob(join("autogen", "*.py"))
    gen_files = [
        output_dir / "auto_paridecl.pxd",
        output_dir / "auto_gen.pxi",
    ]

    if not force and all(exists(f) for f in gen_files):
        src_mtime = max(getmtime(f) for f in src_files)
        gen_mtime = min(getmtime(f) for f in gen_files)

        if gen_mtime > src_mtime:
            return

    G = PariFunctionGenerator(output_dir)
    G()
