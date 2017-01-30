from setuptools import setup
from distutils.command.build_ext import build_ext as _build_ext
from setuptools.extension import Extension

import os
import sys


# Adapted from Cython's new_build_ext
class build_ext(_build_ext):
    def finalize_options(self):
        # Generate auto-generated sources from pari.desc
        from autogen import rebuild
        rebuild()

        from Cython.Build.Dependencies import cythonize
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules, include_path=sys.path)
        _build_ext.finalize_options(self)


setup(
    name='cypari2',
    version='0.1.0a1',
    description='An interface to the number theory library libpari',
    url='https://github.com/defeo/cypari2',
    author='Many people',
    author_email="sage-devel@googlegroups.com",
    license='GNU General Public License, version 2 or later',
    ext_modules=[Extension("*", ["cypari2/*.pyx"])],
    keywords='PARI/GP number theory',
    packages=['cypari2'],
    package_dir={'cypari2': 'cypari2'},
    package_data={'cypari2': ['*.pxi', '*.pxd', '*.h']},
    install_requires=['cysignals'],
    cmdclass=dict(build_ext=build_ext)
)
