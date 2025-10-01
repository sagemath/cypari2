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
  input: 'cypari2.py.in',
  output: 'cypari2.py',
  configuration: config_data,
  install: true,
  install_dir: py.get_install_dir() / 'cypari2'
)
