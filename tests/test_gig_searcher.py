
import gig_searcher

import unittest

class StaticGigSearchSource(gig_searcher.GigSearcherSource):
    "Returns as result, a value previously set in the creation."
    
    def __init__(self, result):
        self.result = result
    
    def search_by_location(self, location):
        return self.result
        
    def search_by_coordinates(self, latitude, longitude):
        return self.result

class TestGigSearcher(unittest.TestCase):
    "Test the class GigSearcher."
    
    def test_gig_search_identity(self):
        # Tests the basic functionality of the GigSearch class, along with the IdentityGigSearchResultTranslator (the default translator used).
        result = {'a': 30, 'b': 10}
        searcher = gig_searcher.GigSearcher(StaticGigSearchSource(result))
        self.assertEquals(result, searcher.search_by_location('test'))
        self.assertEquals(result, searcher.search_by_coordinates(0, 0))
        
        searcher = gig_searcher.GigSearcher(StaticGigSearchSource(result), gig_searcher.IdentityGigSearchResultTranslator())
        self.assertEquals(result, searcher.search_by_location('test'))
        self.assertEquals(result, searcher.search_by_coordinates(0, 0))
        