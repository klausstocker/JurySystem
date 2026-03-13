import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from shared.database import multiline_eval

class TestMultilineEval(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def test_simple(self):
        expr = """
a = 10
b = 20
a + b
"""
        self.assertEqual(multiline_eval(expr), '30')
        
    def test_tuple(self):
        expr = """
goldThres, silberThres, bronzeThres = 30, 20, 10
'gold' if sum > goldThres else 'silber' if sum > silberThres else 'bronze' if sum > bronzeThres else ''
"""
        self.assertEqual(multiline_eval(expr, {'sum' : 5}), '')
        self.assertEqual(multiline_eval(expr, {'sum' : 15}), 'bronze')
        self.assertEqual(multiline_eval(expr, {'sum' : 25}), 'silber')
        self.assertEqual(multiline_eval(expr, {'sum' : 35}), 'gold')


if __name__ == '__main__':
    unittest.main()
