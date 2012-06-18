
import num_util

import unittest

class TestFunctions(unittest.TestCase):
    "Test the functions in the num_util module."
    
    def test_parse_num(self):
        #Test the function 'parse_num(n)'.
        parse_num = num_util.parse_num
        self.assertEquals(0, parse_num('0'))
        self.assertEquals(-4, parse_num('-4'))
        self.assertEquals(1235, parse_num('1235'))
        self.assertEquals(32432423794.5678, parse_num('32432423794.5678'))
        self.assertEquals(-3424234324.4535, parse_num('-3424234324.4535'))
        self.assertEquals(-0.00000000001, parse_num('-0.00000000001'))
        self.assertEquals(None, parse_num('0a'))
        self.assertEquals(None, parse_num('-+4543'))
        self.assertEquals(None, parse_num('--'))
        self.assertEquals(None, parse_num('word'))
        self.assertEquals(None, parse_num('1234 123'))
        self.assertEquals(None, parse_num('12,4'))
