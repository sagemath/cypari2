import sys
from setuptools import setup
from distutils.command.build_ext import build_ext as _build_ext
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.extension import Extension



# Adapted from Cython's new_build_ext
class build_ext(_build_ext):
    def finalize_options(self):
        # Check dependencies
        try:
            from Cython.Build.Dependencies import cythonize
        except ImportError as E:
            sys.stderr.write("Error: {0}\n".format(E))
            sys.stderr.write("The installation of cypari2 requires Cython\n")
            sys.exit(1)

        try:
            # We need the header files for cysignals at compile-time
            import cysignals
        except ImportError as E:
            sys.stderr.write("Error: {0}\n".format(E))
            sys.stderr.write("The installation of cypari2 requires cysignals\n")
            sys.exit(1)

        # Generate auto-generated sources from pari.desc
        from autogen import rebuild
        rebuild()

        self.directives = dict(binding=True)

        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules,
            compiler_directives=self.directives,
            include_path=sys.path)

        _build_ext.finalize_options(self)


class no_egg(_bdist_egg):
    def run(self):
        from distutils.errors import DistutilsOptionError
        raise DistutilsOptionError("The package cypari2 will not function correctly when built as egg. Therefore, it cannot be installed using 'python setup.py install' or 'easy_install'. Instead, use 'pip install' to install cypari2.")


setup(
    name='cypari2',
    version=open("VERSION").read().strip(),
    description='An interface to the number theory library libpari',
    url='https://github.com/defeo/cypari2',
    author='Many people',
    author_email="sage-devel@googlegroups.com",
    license='GNU General Public License, version 2 or later',
    ext_modules=[Extension("*", ["cypari2/*.pyx"])],
    keywords='PARI/GP number theory',
    packages=['cypari2'],
    package_dir={'cypari2': 'cypari2'},
    package_data={'cypari2': ['declinl.pxi', '*.pxd', '*.h']},
    cmdclass=dict(build_ext=build_ext, bdist_egg=no_egg)
)
