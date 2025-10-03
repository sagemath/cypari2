extension_data = {
  'test': files('test.pyx'),
}

foreach name, pyx : extension_data
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'cypari2',
    install: true,
    dependencies: [cysignals, pari],
    include_directories: [inc_root, include_directories('./../cypari2')],
  )
endforeach

