#!/usr/bin/env python

import os

from setuptools import setup
from setuptools.config import read_configuration
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.extension import Extension

from distutils.command.build_ext import build_ext as _build_ext

# read setup keywords from setup.cfg
dir_path = os.path.dirname(os.path.realpath(__file__))
conf_dict = read_configuration(os.path.join(dir_path, "setup.cfg"))
# NOTE: Python2.7 do not support multiple dictionaries unpacking
setup_kwds = conf_dict['metadata']
setup_kwds.update(conf_dict['options'])
# NOTE: Python2.7 parser for setup.cfg does not support wildcards. We
# manually update setup_kwds here
#
# [options.package_data]
#     cypari2 = *.pxd, *.h
#
setup_kwds['package_data'] = {'cypari2': ['*.pxd', '*.h']}

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
        import sys
        sys.path.append(os.curdir)

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
            aliases={'include_dirs': self.compiler_include_dirs,
                     'library_dirs': self.compiler_library_dirs}
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
