#!/usr/bin/env python3
"""
Manager
"""
import unittest
from application import manager, app #pylint: disable=unused-import

@manager.command
def test():
    """Runs unit tests."""
    tests = unittest.TestLoader().discover('application/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
