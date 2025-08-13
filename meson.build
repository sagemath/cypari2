project('cypari2', 'c',
  version: run_command(
    'cat', files('VERSION'),
    check: true
  ).stdout().strip(),
  default_options: ['warning_level=0']
)

# Import Python module
py = import('python').find_installation(pure: false)

# Add dependencies
cython = find_program('cython', required: true)

# Import the dependencies we need  
cysignals_dep = dependency('cysignals', required: false)
cysignals_include_dir = []

if not cysignals_dep.found()
  # Try to find cysignals via Python
  cysignals_result = run_command(
    py.full_path(), '-c', 
    '''
import cysignals
import os
print(os.path.dirname(cysignals.__file__))
    ''',
    check: false
  )
  if cysignals_result.returncode() == 0
    cysignals_include_dir = [cysignals_result.stdout().strip()]
  else
    error('cysignals not found. Please install cysignals.')
  endif
endif

# Get include directories for PARI
pari_include_dirs = []
pari_library_dirs = []

# Try to find PARI using pkg-config
pari_dep = dependency('pari', required: false)

if not pari_dep.found()
  # Fallback: run a Python script to get PARI paths
  pari_paths_result = run_command(
    py.full_path(), '-c',
    '''
import sys, json
sys.path.insert(0, ".")
try:
  from autogen.paths import include_dirs, library_dirs
  result = {"include_dirs": include_dirs(), "library_dirs": library_dirs()}
  print(json.dumps(result))
except Exception as e:
  print(json.dumps({"include_dirs": [], "library_dirs": [], "error": str(e)}))
    ''',
    check: true
  )
  
  pari_json_str = pari_paths_result.stdout().strip()
  # For now, use common paths as fallback
  pari_include_dirs = ['/usr/include', '/usr/local/include']
  pari_library_dirs = ['/usr/lib', '/usr/local/lib', '/usr/lib/x86_64-linux-gnu']
endif

# Include directories
all_include_dirs = pari_include_dirs + cysignals_include_dir
inc_dirs = include_directories(all_include_dirs)

# Run code generation step
code_gen_result = run_command(
  py.full_path(), '-c',
  '''
import sys
sys.path.insert(0, ".")
try:
  from autogen import rebuild
  rebuild(force=True)
  print("Code generation successful")
except Exception as e:
  print("Code generation failed: " + str(e))
  import traceback
  traceback.print_exc()
  ''',
  check: false
)

if code_gen_result.returncode() != 0
  warning('Code generation may have failed: ' + code_gen_result.stdout() + code_gen_result.stderr())
endif

# Define the source files
cython_sources = [
  'cypari2/closure.pyx',
  'cypari2/stack.pyx', 
  'cypari2/custom_block.pyx',
  'cypari2/convert.pyx',
  'cypari2/string_utils.pyx',
  'cypari2/handle_error.pyx',
  'cypari2/gen.pyx',
  'cypari2/pari_instance.pyx'
]

# Create targets for each Cython source file
py_sources = []
foreach src : cython_sources
  basename = src.split('/')[1].split('.')[0]
  c_file = custom_target(basename + '_c',
    input: src,
    output: basename + '.c',
    command: [
      cython, 
      '-3',
      '--capi-reexport-cincludes',
      '-I', meson.current_source_dir() / 'cypari2',
      '@INPUT@',
      '-o', '@OUTPUT@'
    ]
  )
  
  py_ext = py.extension_module(
    basename,
    c_file,
    include_directories: [inc_dirs, 'cypari2'],
    dependencies: [cysignals_dep, pari_dep],
    link_args: ['-lpari'],
    install: true,
    subdir: 'cypari2'
  )
  py_sources += py_ext
endforeach

# Install Python package files
python_sources = [
  'cypari2/__init__.py',
]

py.install_sources(
  python_sources,
  subdir: 'cypari2'
)

# Install package data files
package_data = [
  'cypari2/closure.pxd',
  'cypari2/convert.pxd',
  'cypari2/gen.pxd',
  'cypari2/handle_error.pxd',
  'cypari2/pari_instance.pxd',
  'cypari2/paridecl.pxd',
  'cypari2/paripriv.pxd',
  'cypari2/pycore_long.pxd',
  'cypari2/stack.pxd',
  'cypari2/string_utils.pxd',
  'cypari2/types.pxd',
  'cypari2/cypari.h',
  'cypari2/pycore_long.h',
]

# Check if auto-generated files exist and install them
auto_files = [
  'cypari2/auto_paridecl.pxd',
  'cypari2/auto_gen.pxi',
  'cypari2/auto_instance.pxi',
]

foreach f : auto_files
  if import('fs').is_file(f)
    package_data += f
  endif
endforeach

py.install_sources(
  package_data,
  subdir: 'cypari2',
  preserve_path: false
)