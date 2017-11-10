import unittest
import sys
from cypari2 import Pari, PariError

pari = Pari()

testmodules = [
    'bern',
    'bestappr',
    'set',
    'polylog',
    'subcyclo',
    'characteristic',
    'chinese',
    'disc',
    'ellanal',
    'ellmodulareqn',
    'factorint',
    'gamma',
    'galpol',
    'idealappr',
    'idealramgroups',
    'isprime',
    'lambert',
    'lex',
    'lindep',
    'linear',
    'list',
    'log',
    'mathnf',
    'contfrac',
    'minim',
    'minmax',
    'modfun',
    'modular',
    'nfrootsof1',
    'nfsplitting',
    'norm',
    'number',
    'pol',
    'prec',
    'prime',
    'primes',
    'qfb',
    'qfbclassno',
    'qfsolve',
    'quadray',
    'rootsreal',
    'ser',
    'subst',
    'sumdedekind',
    'sumformal',
    'zeta',
    'polred',
    'bit',
    'charpoly'
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
    if not ((t in require_galpol and not galpol_installed) or (t in require_seadata and not seadata_installed)):
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

res = unittest.TextTestRunner().run(suite)
retcode = 0 if res.wasSuccessful() else 1
sys.exit(retcode)
