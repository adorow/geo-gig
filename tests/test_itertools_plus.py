
import itertools_plus

import unittest

class TestFunctions(unittest.TestCase):
    "Test the functions in the itertools_plus module."
    
    def test_group_by(self):
        #Test the function 'group_by(list, key)'.
        group_by = itertools_plus.group_by
        identity = lambda a: a
        self.assertEquals({ 'A': ['A', 'A'], 'B': ['B', 'B'], 'C': ['C', 'C'], 'D': ['D', 'D'] }, group_by('ABCDDACB', key=identity))
        self.assertEquals({ 'A': ['A', 'A'], 'B': ['B', 'B'], 'C': ['C', 'C'], 'D': ['D', 'D'] }, group_by(['A', 'B', 'C', 'D', 'D', 'A', 'C', 'B'], key=identity))
        
        get_a_b = lambda a: a['a']['b']
        v1 = {'id':1,'a':{'b':30, 'c':40}}
        v2 = {'id':2,'a':{'b':20, 'c':30}, 'b': 30}
        v3 = {'id':3,'a':{'b':30, 'c':30}}
        v4 = {'id':4,'a':{'b':20, 'c':20}, 'b': 30}
        self.assertEquals({20: [v2, v4], 30: [v1, v3]}, group_by([v1, v2, v3, v4], key=get_a_b))