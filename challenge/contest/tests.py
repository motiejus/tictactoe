import doctest
from challenge.contest import logic


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(logic))
    return tests
