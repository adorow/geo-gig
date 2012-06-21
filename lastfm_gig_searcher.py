
import json

from lastfm_little_wrapper import Lastfm
from gig_searcher import *
from geogig_format_util import get_coordinate_from_event

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
        lastfm_json_response = self._lastfm.geo().get_events(location=(location if not (latitude and longitude) else None), latitude=latitude, longitude=longitude, limit=50)
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
        
        geogig_events = [self._translate_event(lastfm_event) for lastfm_event in events_list]
        return geogig_events
        
    def _translate_event(self, lastfm_event): 
        event = {}
        
        event['title'] = lastfm_event['title'] if 'title' in lastfm_event else None
        
        large_images = [image['#text'] for image in lastfm_event['image'] if image['size'] == 'large']
        event['image_url'] = large_images[0] if len(large_images) > 0 else None
        
        event['url'] = lastfm_event['website'] if ('website' in lastfm_event and lastfm_event['website']) else lastfm_event['url'] if ('url' in lastfm_event and lastfm_event['url']) else None
        
        event['cancelled'] = True if ('cancelled' in lastfm_event and lastfm_event['cancelled'] == '1') else False
        
        event['date'] = lastfm_event['startDate'] if 'startDate' in lastfm_event else None
        
        if 'artists' not in lastfm_event or 'artist' not in lastfm_event['artists']:
            event['artists'] =  []
        else:
            artists = lastfm_event['artists']['artist']
            event['artists'] =  [self._translate_artist(artist) for artist in artists] if isinstance(artists, list) else [self._translate_artist(artists)]
        
        event['venue'] = self._translate_venue(lastfm_event['venue']) if 'venue' in lastfm_event else None
        
        return event
        
    def _translate_artist(self, lastfm_artist):
        artist = {
            'name' : lastfm_artist,
            'url': 'http://www.last.fm/music/' + lastfm_artist.replace(' ', '+')
        }
        
        return artist
    
    def _translate_venue(self, lastfm_venue):
        venue = {}
        
        venue['name'] = lastfm_venue['name'] if 'name' in lastfm_venue else None
        venue['phonenumber'] = lastfm_venue['phonenumber'] if 'phonenumber' in lastfm_venue else None
        venue['url'] = lastfm_venue['website'] if ('website' in lastfm_venue and lastfm_venue['website']) else lastfm_venue['url'] if ('url' in lastfm_venue and lastfm_venue['url']) else None
        venue['location'] = self._translate_location(lastfm_venue['location']) if 'location' in lastfm_venue else None
        
        return venue
        
    def _translate_location(self, lastfm_location):
        location = {}
        
        location['street'] = lastfm_location['street'] if 'street' in lastfm_location else None
        location['postalcode'] = lastfm_location['postalcode'] if 'postalcode' in lastfm_location else None
        location['city'] = lastfm_location['city'] if 'city' in lastfm_location else None
        location['country'] = lastfm_location['country'] if 'country' in lastfm_location else None
        location['coordinates'] = self._translate_coordinates(lastfm_location['geo:point']) if 'geo:point' in lastfm_location else None
        
        return location
        
    def _translate_coordinates(self, lastfm_coordinates):
        coordinates = {
            'latitude': lastfm_coordinates['geo:lat'] if 'geo:lat' in lastfm_coordinates else None,
            'longitude': lastfm_coordinates['geo:long'] if 'geo:long' in lastfm_coordinates else None            
        }
        
        return coordinates
        