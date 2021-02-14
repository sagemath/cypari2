#!/usr/bin/env python

import sys, os

from setuptools import setup
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.extension import Extension

from distutils.command.build_ext import build_ext as _build_ext

# NOTE: Python2.7 parser for setup.cfg does not support wildcards. We
# manually update setup_kwds here
#
# [options.package_data]
#     cypari2 = *.pxd, *.h
#
setup_kwds = {
    'package_data': {'cypari2': ['*.pxd', '*.h']}
}

if "READTHEDOCS" in os.environ:
    # When building with readthedocs, disable optimizations to decrease
    # resource usage during build
    ext_kwds["extra_compile_args"] = ["-O0"]

    # Print PARI/GP defaults and environment variables for debugging
    from subprocess import Popen, PIPE
    Popen(["gp", "-f", "-q"], stdin=PIPE).communicate(b"default()")
    for item in os.environ.items():
        print("%s=%r" % item)


# Adapted from Cython's new_build_ext
class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)

        # Let the current repository be part of the module search
        # (otherwise autogen is not found)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(dir_path)

        # Generate auto-generated sources from pari.desc
        from autogen import rebuild
        rebuild()

        self.compiler_directives = {
            "autotestdict.cdef": True,
            "binding": True,
            "cdivision": True,
            "language_level": 2,
        }

        from autogen.paths import include_dirs, library_dirs
        self.compiler_include_dirs = include_dirs()
        self.compiler_library_dirs = library_dirs()

    def run(self):
        # Run Cython
        from Cython.Build.Dependencies import cythonize
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules,
            compiler_directives=self.compiler_directives,
            aliases={'INCLUDE_DIRS': self.compiler_include_dirs,
                     'LIBRARY_DIRS': self.compiler_library_dirs}
            )

        _build_ext.run(self)

class no_egg(_bdist_egg):
    def run(self):
        from distutils.errors import DistutilsOptionError
        raise DistutilsOptionError("The package cypari2 will not function correctly when built as egg. Therefore, it cannot be installed using 'python setup.py install' or 'easy_install'. Instead, use 'pip install' to install cypari2.")


setup(
    version=VERSION,
    setup_requires=['Cython>=0.29'],
    install_requires=['cysignals>=1.7'],
    long_description=README,
    ext_modules=[Extension("*", ["cypari2/*.pyx"])],
    cmdclass=dict(build_ext=build_ext, bdist_egg=no_egg),
    **setup_kwds
)
