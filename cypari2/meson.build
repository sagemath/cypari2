py.install_sources(
  '__init__.py',
  '_thread_runtime.py',
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
  'thread_support.pxd',
  'types.pxd',
  'cypari.h',
  'pycore_long.h',
  subdir: 'cypari2'
)


extension_data = {
  'closure': files('closure.pyx'),
  'stack': files('stack.pyx'),
  'custom_block': files('custom_block.pyx'),
  'thread_support': files('thread_support.pyx'),
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
    dependencies: [py.dependency(), cysignals, pari, threads],
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
configure_file(
  input: '__init__.py',
  output: '__init__.py',
  copy: true,
)
configure_file(
  input: '_thread_runtime.py',
  output: '_thread_runtime.py',
  copy: true,
)

# pkg-config file describing the PARI library that cypari2 is linked against,
# so that other projects (e.g. Sage) can use the same PARI library.
# When building binary wheels, tools/bundle_pari_devel.py replaces it by a file
# pointing to the PARI library and headers bundled in the wheel.
pari_pc_cflags = []
foreach dir : pari_header_dirs
  pari_pc_cflags += '-I' + dir
endforeach
pari_pc_libs = []
foreach dir : pari_lib_dirs
  pari_pc_libs += '-L' + dir
endforeach
pari_pc_libs += '-lpari'
config_data_pari = configuration_data()
config_data_pari.set('pari_version', pari_version_str)
config_data_pari.set('pari_cflags', ' '.join(pari_pc_cflags))
config_data_pari.set('pari_libs', ' '.join(pari_pc_libs))
configure_file(
  input: 'pari.pc.in',
  output: 'pari.pc',
  configuration: config_data_pari,
  install: true,
  install_dir: py.get_install_dir() / 'cypari2'
)
