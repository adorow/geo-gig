import json

from lastfm_little_wrapper import Lastfm

class GigSearchException(Exception):
    "Exception raised when an error occurs on the gig search."
    def __init__(self, service, strerror):
        self.service = service
        self.strerror = strerror

class GigSearcher:
    "Defines a GigSearcher. An implementation of this abstract class is able to search for gigs given some localization parameters."
    
    def searchByLocation(self, location):
        "Search for gigs next to a given location."
        raise NotImplementedError("Should have implemented this")
        
    def searchByCoordinates(self, latitude, longitude):
        "Search for gigs next to a given geographical position."
        raise NotImplementedError("Should have implemented this")
        
class LastfmGigSearcher(GigSearcher):
    "A GigSearcher that uses the Last.fm API to search for gigs."

    def __init__(self, api_key):
        if not api_key:
            raise ValueError('An API key needs to be informed to use Last.fm web services.')
        self._lastfm =  Lastfm(api_key, 'json')
        
    def searchByLocation(self, location):
        return self._search(location=location)
        
    def searchByCoordinates(self, latitude, longitude):
        return self._search(latitude=latitude, longitude=longitude)
        
    def _search(self, location=None, latitude=None, longitude=None):
        # TODO: find a service (maybe google has one) that identifies the latitude and longitude of a place from a string with the location name. (take a look at https://developers.google.com/maps/documentation/javascript/reference#Geocoder and https://developers.google.com/maps/documentation/geocoding/), an example of using the geocoding api: http://maps.googleapis.com/maps/api/geocode/json?address=Dublin,%20Ireland&sensor=false
    
        # TODO: have to make this better. Is very messy (and very ugly. Most of it, at least). A massive refactor is probably on the way... reminder: binsearch idea with distance and limit. 
   
        # location should be sent only if latitude and longitude are not, because when location is informed, the Last.fm API always use this, and ignores latitude and longitude
        lastfm_json_response = self._lastfm.geo().get_events(location=(location if not (latitude and longitude) else None), latitude=latitude, longitude=longitude, limit=30)
        events_dict = json.loads(lastfm_json_response)
        
        #print events_dict['events']['@attr']  # TODO: his can show the parameters used on the search by Last.fm. Maybe this information can be used for something useful.
        
        # TODO: the following tells if the response is an error, it needs to be refactored into a method though:
        if 'error' in events_dict:
            raise GigSearchException('Last.fm [Geo.getEvents]',  '[Error ' + str(events_dict['error']) + '] ' + events_dict['message'])
           
        # if there's only one event here, it will be the object event, otherwise, it'll be a list of events
        events_list = events_dict['events']['event'] 
        # so, if it's not a list, we make it one
        if not isinstance(events_list, list):
            events_list = [events_list]
        
        # remove events with empty coordinates (TODO: check if its possible to use those events anyway, maybe find its coordinates with another service [is there a google maps search?], or show it differently)
        events_list = filter(lambda e: e['venue']['location']['geo:point']['geo:lat'] and e['venue']['location']['geo:point']['geo:long'], events_list) 
        
        return events_list