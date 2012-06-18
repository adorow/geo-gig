
import geocoding

import unittest

class StaticGeocodingSource(geocoding.GeocodingSource):
    "Returns as result, a value previously set in the creation."
    
    def __init__(self, result):
        self.result = result
    
    def find_by_location(self, location):
        return self.result
        
    def find_by_coordinates(self, latitude, longitude):
        return self.result

class TestGeocoder(unittest.TestCase):
    "Test the class Geocoder."
    
    def test_gig_search_identity(self):
        # Tests the basic functionality of the GigSearch class, along with the IdentityGigSearchResultTranslator (the default translator used).
        result = {'a': 30, 'b': 10}
        searcher = geocoding.Geocoder(StaticGeocodingSource(result))
        self.assertEquals(result, searcher.find_by_location('test'))
        self.assertEquals(result, searcher.find_by_coordinates(0, 0))
        
        searcher = geocoding.Geocoder(StaticGeocodingSource(result), geocoding.IdentityGeocodingResultTranslator())
        self.assertEquals(result, searcher.find_by_location('test'))
        self.assertEquals(result, searcher.find_by_coordinates(0, 0))
        