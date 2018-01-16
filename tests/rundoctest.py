#!/usr/bin/env python

import os
import sys

# Autogen tests must be run in the root dir, and with the proper module path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
os.chdir(path)
sys.path.append(path)
import autogen
import cypari2
import doctest

# The doctests assume utf-8 encoding
cypari2.string_utils.encoding = "utf-8"

# For doctests, we want exceptions to look the same,
# regardless of the Python version. Python 3 will put the
# module name in the traceback, which we avoid by faking
# the module to be __main__.
cypari2.handle_error.PariError.__module__ = "__main__"

failed = 0
attempted = 0
for mod in [cypari2.closure, cypari2.convert, cypari2.gen,
            cypari2.handle_error, cypari2.pari_instance, cypari2.stack,
            cypari2.string_utils,
            autogen.doc, autogen.generator, autogen.parser,
            autogen.paths]:

    print("="*80)
    print("Testing {}".format(mod.__name__))
    test = doctest.testmod(mod, optionflags=doctest.ELLIPSIS|doctest.REPORT_NDIFF)
    failed += test.failed
    attempted += test.attempted

print("="*80)
print("Summary result for cypari2:")
print("   attempted = {}".format(attempted))
print("   failed = {}".format(failed))

sys.exit(failed)
