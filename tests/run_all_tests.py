import unittest

suite = unittest.TestLoader().discover('.', pattern='test_*.py', top_level_dir=None)

print 'Starting execution of', suite.countTestCases(), 'test cases.\n'
unittest.TextTestRunner(verbosity=2).run(suite)