from __future__ import absolute_import

import glob
import os
from os.path import join, getmtime, exists

from .generator import PariFunctionGenerator
from .parser import pari_share


def rebuild(force=False):
    pari_module_path = 'cypari2'
    src_files = [join(pari_share(), b'pari.desc')] + \
                 glob.glob(join('autogen', 'pari', '*.py'))
    gen_files = [join(pari_module_path, 'auto_gen.pxi')]

    if all(exists(f) for f in gen_files):
        src_mtime = max(getmtime(f) for f in src_files)
        gen_mtime = min(getmtime(f) for f in gen_files)

        if gen_mtime > src_mtime and not force:
            return

    G = PariFunctionGenerator()
    G()
