import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.publish

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('queue.txt',
                     package=sparc.publish),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')