project('cypari2', 
  ['c', 'cython'],
  version: files('VERSION'),
  license: 'GPL v2+',
  default_options: ['c_std=c17', 'python.install_env=auto'],
  meson_version: '>=1.2',
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
# Cannot be found via pkg-config
pari = cc.find_library('pari', required: true)

# Run code generation step
code_gen_result = run_command(
  py.full_path(), '-c',
  '''
import sys
sys.path.insert(0, ".")
from autogen import rebuild
rebuild(force=True)
print("Code generation successful")
  ''',
  check: true
)

subdir('cypari2')
