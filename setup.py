from setuptools import setup
from distutils.command.build_ext import build_ext as _build_ext
from distutils.sysconfig import get_python_inc
from setuptools.extension import Extension
from Cython.Build.Dependencies import cythonize
import autogen

import os, sys
from glob import glob

opj = os.path.join

cythonize_dir = "build"

kwds = dict(include_dirs=["cypari2"],# cythonize_dir, opj(cythonize_dir, "cypari2")],
            libraries=["pari"],
            depends=glob(opj("cypari2", "*.h")))

extensions = [
    Extension("cypari2.closure", ["cypari2/closure.pyx"], **kwds),
    Extension("cypari2.convert", ["cypari2/convert.pyx"], **kwds),
    Extension("cypari2.gen", ["cypari2/gen.pyx"], **kwds),
    Extension("cypari2.handle_error", ["cypari2/handle_error.pyx"], **kwds),
    Extension("cypari2.pari_instance", ["cypari2/pari_instance.pyx"], **kwds),
    Extension("cypari2.stack", ["cypari2/stack.pyx"], **kwds),
]

class build_ext(_build_ext):
    def run(self):
        # Generate auto_gen.pxi and auto_instance.pxi
        autogen.rebuild()
        return _build_ext.run(self)

setup(
    name='cypari2',
    version='0.1.0a1',
    description='An interface to the number theory library libpari',
    url='https://github.com/defeo/cypari2',
    author='Many people',
    author_email="sage-devel@googlegroups.com",
    license='GNU General Public License, version 3 or later',
    # Install cycsignals before this
    ext_modules=cythonize(extensions, include_path=sys.path),
    keywords='PARI/gp number theory',
    packages=['cypari2'],
    package_dir={'cypari2': 'cypari2'},
    package_data={'cypari2': ['*.pxi', '*.pxd', '*.h']},
    install_requires=['cysignals'],
    cmdclass=dict(build_ext=build_ext)
)
