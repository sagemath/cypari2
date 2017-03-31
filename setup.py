import sys
from setuptools import setup
from distutils.command.build_ext import build_ext as _build_ext
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

        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules, include_path=sys.path)
        _build_ext.finalize_options(self)


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
    cmdclass=dict(build_ext=build_ext)
)
