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
  'auto_paridecl.pxd',
  'auto_gen.pxi',
  'auto_instance.pxi',
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

foreach name, pyx : extension_data
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'cypari2',
    install: true,
    dependencies: [cysignals, pari],
  )
endforeach

