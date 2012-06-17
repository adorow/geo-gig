
import json

from lastfm_little_wrapper import Lastfm
from gig_searcher import *

class LastfmGigSearcherSource(GigSearcherSource):
    "Class that uses the Last.fm API as a source to search for gigs."

    def __init__(self, api_key):
        "Creates the Source using an API key."
        if not api_key:
            raise ValueError('An API key needs to be informed to use Last.fm web services.')
        self._lastfm =  Lastfm(api_key, 'json')
        
    def search_by_location(self, location):
        return self._search(location=location)
        
    def search_by_coordinates(self, latitude, longitude):
        return self._search(latitude=latitude, longitude=longitude)
        
    def _search(self, location=None, latitude=None, longitude=None):
        # location should be sent only if latitude and longitude are not, because when location is informed, the Last.fm API always use this, and ignores latitude and longitude
        lastfm_json_response = self._lastfm.geo().get_events(location=(location if not (latitude and longitude) else None), latitude=latitude, longitude=longitude, limit=30)
        events_dict = json.loads(lastfm_json_response)
        
        if 'error' in events_dict:
            raise GigSearchException('Last.fm [Geo.getEvents]',  '[Error ' + str(events_dict['error']) + '] ' + events_dict['message'])
        
        return events_dict
        
class LastfmGigSearchResultTranslator(GigSearchResultTranslator):
    "Class that translates the results from the Last.fm API to the format that geo-gig understands (defined in geogig-search-result-format.txt)."

    def translate(self, lastfm_result):
        if 'events' not in lastfm_result or not 'event' in lastfm_result['events']:
            raise GigSearchException('Last.fm [Geo.getEvents]', 'Error processing the results received from the service.')
        
        # if there's only one event here, it will be the object event, otherwise, it'll be a list of events
        events_list = lastfm_result['events']['event'] 
        # so, if it's not a list, we make it one
        if not isinstance(events_list, list):
            events_list = [events_list]
        
        events_list = filter(lambda e: e['venue']['location']['geo:point']['geo:lat'] and e['venue']['location']['geo:point']['geo:long'], events_list) 
        
        return events_list