py.install_sources(
  '__init__.py',
  'closure.pxd',
  'convert.pxd',
  'gen.pxd',
  'handle_error.pxd',
  'pari_instance.pxd',
  'paridecl.pxd',
  'paripriv.pxd',
  'pycore_long.pxd',
  'stack.pxd',
  'string_utils.pxd',
  'types.pxd',
  'cypari.h',
  'pycore_long.h',
  subdir: 'cypari2'
)

pari_header_search_roots = []
if host_machine.system() == 'darwin'
  pari_header_search_roots += ['/opt/homebrew/include', '/usr/local/include']
elif host_machine.system() == 'windows'
  pari_header_search_roots += ['/ucrt64/include']
else
  multiarch_include_root = run_command(cc, '-print-multiarch', check: false).stdout().strip()
  if multiarch_include_root != ''
    pari_header_search_roots += ['/usr/include/' + multiarch_include_root]
  endif
  pari_header_search_roots += ['/usr/include', '/usr/local/include']
endif

pari_header_root = run_command(
  py,
  [
    '-c',
    '''
import os
import sys

seen = set()
for root in sys.argv[1:]:
    if root in seen:
        continue
    seen.add(root)
    if os.path.exists(os.path.join(root, "pari", "pari.h")):
        print(root)
        break
    '''.strip(),
  ] + pari_header_search_roots,
  check: true,
).stdout().strip()

if pari_header_root != ''
  install_subdir(
    pari_header_root + '/pari',
    install_dir: py.get_install_dir() / 'cypari2',
  )
else
  warning('Could not locate PARI headers to install alongside pari.pc')
endif


extension_data = {
  'closure': files('closure.pyx'),
  'stack': files('stack.pyx'),
  'custom_block': files('custom_block.pyx'),
  'convert': files('convert.pyx'),
  'string_utils': files('string_utils.pyx'),
  'handle_error': files('handle_error.pyx'),
  'gen': files('gen.pyx'),
  'pari_instance': files('pari_instance.pyx')
}

inc_src = include_directories('.')
# Meson currently ignores include_directories for Cython modules, so we
# have to add them manually.
# https://github.com/mesonbuild/meson/issues/9562
add_project_arguments('-I', meson.current_source_dir(), language: 'cython')
add_project_arguments('-I', meson.current_build_dir(), language: 'cython')

foreach name, pyx : extension_data
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'cypari2',
    install: true,
    dependencies: [cysignals, pari],
    include_directories: [inc_root, inc_src],
  )
endforeach

config_data = configuration_data()
config_data.set('version', meson.project_version())
configure_file(
  input: 'cypari2.pc.in',
  output: 'cypari2.pc',
  configuration: config_data,
  install: true,
  install_dir: py.get_install_dir() / 'cypari2'
)

config_data_pari = configuration_data()
config_data_pari.set('pari_version', pari_version_str)
configure_file(
  input: 'pari.pc.in',
  output: 'pari.pc',
  configuration: config_data_pari,
  install: true,
  install_dir: py.get_install_dir() / 'cypari2'
)
