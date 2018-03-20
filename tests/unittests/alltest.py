"""
    alltest.py : Launch unittests modules in ``testmodules`` list. 

    Each test module corresponds to a PARI-GP test file that was ported into a gmpy2 unittest.
"""
import unittest
import sys
from cypari2 import Pari, PariError

pari = Pari()

testmodules = [
    'bern',
    'bit',
    'characteristic',
    'charpoly',
    'chinese',
    'contfrac',
    'disc',
    'ellmodulareqn',
    'factorint',
    'galpol',
    'idealappr',
    'isprime',
    'lambert',
    'lex',
    'lindep',
    'linear',
    'list',
    'log',
    'mathnf',
    'minim',
    'minmax',
    'modfun',
    'modular',
    'nfrootsof1',
    'norm',
    'number',
    'pol',
    'prec',
    'prime',
    'primes',
    'qfb',
    'qfbclassno',
    'qfsolve',
    'set',
    'subcyclo',
    'sumdedekind',
    'sumformal',
    'zeta'
    ]

require_galpol = ["galpol"]
require_seadata = ["ellmodulareqn"]

galpol_installed = True
seadata_installed = True

# test extensions presence.
try:
    pari.ellmodulareqn(2)
except PariError as e:
    if "error opening seadata file" in str(e):
        seadata_installed = False
    else:
        raise e

try:
    pari.galoisgetpol(8)
except PariError as e:
    if "error opening galpol file" in str(e):
        galpol_installed = False
    else:
        raise e

suite = unittest.TestSuite()


for t in testmodules:
    if (galpol_installed or t not in require_galpol) and (seadata_installed or t not in require_seadata):
        # Load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

res = unittest.TextTestRunner().run(suite)
retcode = 0 if res.wasSuccessful() else 1
sys.exit(retcode)
