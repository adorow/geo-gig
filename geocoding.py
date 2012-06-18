
class GeocodingException(Exception):
    "Exception raised when an error occurred while trying to execute a Geocoding service."
    def __init__(self, service, strerror):
        self.service = service
        self.strerror = strerror

class GeocodingResult:
    "The result of a geocoding search."

    def __init__(self, location, latitude, longitude):
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

class GeocodingSource:
    "Defines a source of geocoding data."
    
    def find_by_location(self, location):
        """ Returns a GeocodingResult for a given location, or raises an exception, in case the location could not be found.
           
            location: the location being searched.
        """
        raise NotImplementedError("Should have implemented this")
        
    def find_by_coordinates(self, latitude, longitude):
        """ Returns a GeocodingResult for a given latitude and longitude, or raises an exception, in case the location could not be found.
           
            latitude: the latitude of the location being searched.
            longitude: the longitude of the location being searched.
        """
        raise NotImplementedError("Should have implemented this")
    

class GeocodingResultTranslator:
    "Defines a translator of geocoding result."
    
    def translate(self, source_result):
        "Translate the result from the source into a result that geo-gig will understand."
        raise NotImplementedError("Should have implemented this")

class IdentityGeocodingResultTranslator(GeocodingResultTranslator):
    "A translator that simply returns the result given by the source, it basically considers that the result is already in the expected format."
    
    def translate(self, source_result):
        return source_result   
 
class Geocoder:
    "Base class for Geocoding."
    def __init__(self, source, translator=IdentityGeocodingResultTranslator()):
        "Creates a new GigSearcher."
        self._source = source
        self._translator = translator
    
    def find_by_location(self, location):
        return self._translator.translate(self._source.find_by_location(location))
        
    def find_by_coordinates(self, latitude, longitude):
        return self._translator.translate(self._source.find_by_coordinates(latitude, longitude))
    