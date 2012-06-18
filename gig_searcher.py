
class GigSearchException(Exception):
    "Exception raised when an error occurs on the gig search."
    def __init__(self, service, strerror):
        self.service = service
        self.strerror = strerror

class GigSearcherSource:
    "Defines a source for a GigSearch. Basically is the real request for the data."
    
    def search_by_location(self, location):
        "Search for gigs next to a given location. This function may raise a GigSearchException, if some problem occurs on the search."
        raise NotImplementedError("Should have implemented this")
        
    def search_by_coordinates(self, latitude, longitude):
        "Search for gigs next to a given geographical position. This function may raise a GigSearchException, if some problem occurs on the search."
        raise NotImplementedError("Should have implemented this")

class GigSearchResultTranslator:
    "Defines a translator of gig search results. The role of the implementation of this class is to transform the data returned from a Source into data that geo-gig can understand. In other words, transforms the source's data into the format defined in geogig-search-result-format.txt"
    
    def translate(self, source_result):
        "Translate the result from the source into a result that geo-gig will understand."
        raise NotImplementedError("Should have implemented this")

class IdentityGigSearchResultTranslator(GigSearchResultTranslator):
    "A translator that simply returns the result given by the source, it basically considers that the result is already in the expected format."
    
    def translate(self, source_result):
        return source_result
        
class GigSearcher:
    "Defines a GigSearcher. An implementation of this abstract class is able to search for gigs given some localization parameters."
    
    def __init__(self, source, translator=IdentityGigSearchResultTranslator()):
        "Creates a new GigSearcher."
        self._source = source
        self._translator = translator
    
    def search_by_location(self, location):
        "Search for gigs in a given location."
        return self._translate_result(self._source.search_by_location(location))
        
    def search_by_coordinates(self, latitude, longitude):
        "Search for gigs next to a given coordinate."
        return self._translate_result(self._source.search_by_coordinates(latitude, longitude))
        
    def _translate_result(self, source_result):
        return self._translator.translate(source_result)
