project('cypari2', 
  ['c', 'cython'],
  version: files('VERSION'),
  license: 'GPL v2+',
  default_options: ['c_std=c17', 'python.install_env=auto'],
  meson_version: '>=1.5.0',
)

# Python module
# https://mesonbuild.com/Python-module.html
py = import('python').find_installation(pure: false)

# Compilers
cc = meson.get_compiler('c')
cython = meson.get_compiler('cython')
# Workaround as described in https://cython.readthedocs.io/en/latest/src/userguide/special_methods.html#arithmetic-methods
add_project_arguments('-X c_api_binop_methods=True', language: 'cython')

# Dependencies  
inc_cysignals = run_command(
  py,
  [
    '-c',
    '''
from os.path import relpath
import cysignals
path = cysignals.__file__.replace('__init__.py', '')
try:
  print(relpath(path))
except Exception:
  print(path)
    '''.strip(),
  ],
  check: true,
).stdout().strip()
cysignals = declare_dependency(include_directories: inc_cysignals)
run_command(cc,'-v', check:true)
cc.has_header('pari/pari.h', required: true, args: ['-v'])
# GMP may be a dependency of Pari, but since Pari doesn't have a pkg-config file,
# we have to find it ourselves.
gmp = dependency('gmp', required: false)
# Cannot be found via pkg-config
pari = cc.find_library('pari', has_headers: ['pari/pari.h'], required: false)
if not pari.found()
  # On Windows, the library is named libpari.dll
  pari = cc.find_library('libpari', has_headers: ['pari/pari.h'], required: true)
endif
pari = declare_dependency(dependencies: [pari, gmp])
# Get PARI version (mostly as smoke test)
pari_version_code = '''
#include <stdio.h>
#include <pari/pari.h>
int main(void) {
  pari_init(1000000, 2);
  GEN v = pari_version();
  const char *version = GENtostr(pari_version());
  pari_printf("%s",version);
  pari_close();
  return 0;
}
'''
pari_version = cc.run(
  pari_version_code,
  name: 'pari version',
  dependencies: [pari],
  required: true,
)
message('PARI Version: ' + pari_version.stdout())

pari_datadir_code = '''
#include <stdio.h>
#include <pari/pari.h>
int main(void) {
  pari_init(1000000, 2);
  pari_printf("%s", pari_datadir);
  pari_close();
  return 0;
}
'''
pari_datadir = cc.run(
  pari_datadir_code,
  name: 'pari datadir',
  dependencies: [pari],
  required: true,
).stdout()

# In MSYS, convert to Windows path
# (e.g /usr/share/pari -> C:\msys64\usr\share\pari)
if host_machine.system() == 'windows'
  pari_datadir = run_command(
    'cygpath', '-am', pari_datadir,
    check: true,
  ).stdout().strip()
endif
message('PARI Datadir: ' + pari_datadir)

# Run code generation step
code_gen_result = run_command(
  py.full_path(), '-c',
  '''
import sys
sys.path.insert(0, ".")
from autogen import rebuild
rebuild(r"''' + pari_datadir + '''", force=True, output=r"''' + meson.current_build_dir() + '''/cypari2")
print("Code generation successful")
  ''',
  check: true
)
py.install_sources(
  meson.current_build_dir() + '/cypari2/auto_paridecl.pxd',
  meson.current_build_dir() + '/cypari2/auto_gen.pxi',
  meson.current_build_dir() + '/cypari2/auto_instance.pxi',
  subdir: 'cypari2'
)
inc_root = include_directories('.')
# Meson currently ignores include_directories for Cython modules, so we
# have to add them manually.
# https://github.com/mesonbuild/meson/issues/9562
add_project_arguments('-I', meson.current_source_dir(), language: 'cython')
add_project_arguments('-I', meson.current_build_dir(), language: 'cython')


subdir('cypari2')
