
import logging
import urllib2
import json

from geocoding import *

class GMapsGeocodingSource(GeocodingSource):
    "Uses Google Maps API as a source for geocoding."
    
    def __init__(self):
        self._api_base_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&'
    
    def find_by_location(self, location):
        return self._find('address=' + location.replace(' ', '%20'))
        
    def find_by_coordinates(self, latitude, longitude):
        return self._find('latlng=' + str(latitude) + ',' + str(longitude))
        
    def _find(self, param):
        url = self._api_base_url + param
        logging.debug('Url for GMaps Geocoding request built: ' + url)
        result = urllib2.urlopen(url).read()
        logging.debug('Response from GMaps Geocoding: ' + result)
    
        return json.loads(result)

class GMapsGeocodingResultTranslator(GeocodingResultTranslator):
    "Defines a translator of geocoding result."
    
    def translate(self, source_result):
        "Translates the GoogleMaps API response to a GeocodingResult."
        
        status = source_result['status']
        if status != 'OK':
            raise GeocodingException('Google Maps [Geocoding]', 'The request returned error with status ' + status)
        
        first_result = source_result['results'][0]
        location_name = first_result['formatted_address']
        first_result_coord = first_result['geometry']['location']
        latitude = first_result_coord['lat']
        longitude = first_result_coord['lng']
        
        return GeocodingResult(location_name, latitude, longitude)
        