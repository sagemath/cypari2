import unittest

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
    'bit'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
