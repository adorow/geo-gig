
import logging
import urllib2

# TODO some functions to be added in the (hopefully) near future:
# - Venue.getEvents         |-> Next events in a Venue
# - Venue.search            |-> Search for venues
# - Artist.getEvents        |-> Next events from a given artist
# - Artist.getCorrection    |-> Auto correction for artist names
# - Artist.search           |-> Search artists, returns results by relevance
# - Artist.getInfo
# - Event.getInfo           |-> Informations about events (Geo.getEvents already has those, I think)

API_ROOT_URL = 'http://ws.audioscrobbler.com/2.0/'

class Lastfm:
    """
        A small Last.fm wrapper for using the Last.fm web services.
       
       IMPORTANT: This API does NOT cover Last.fm services that require authentication! 
    """
    
    def __init__(self, api_key, format=None):
        self._api_key = api_key    
        self._format = format
    
    def geo(self):
        """ Creates an instance of the Geo service.
        """
        return self.Geo(self)
    
    def get(self, method_name, params={}):
        """ Executes a Last.fm web service with the given method name and its parameters. It's prefered for the methods in the classes to be used, instead of using directly this one. For example, if you want to use the Geo.getEvents method, use: lastfm.geo().get_events(...) instead of using this get() directly.
            
            @arguments
            method_name: the name of the Lastfm method, as described in the lastfm API documentation. 
            params: the parameters used in the request.
        """
        if not method_name:
            raise ValueError('A method name needs to be informed.')
        
        url = self._build_url(method_name, params)
        logging.debug('Url for Last.fm request built: ' + url)
        result = urllib2.urlopen(url).read()
        logging.debug('Response from Last.fm: ' + result)
        return result
    
    def _build_url(self, method_name, other_params):
        url = API_ROOT_URL + '?'
        
        def _normalize_value(value):
            return value.replace(' ', '%20')
        
        def _as_param(key, value):
            return '&' + key + '=' + _normalize_value(value)
        
        url += _as_param('method', method_name)
        if self._format:
            url += _as_param('format', self._format)
        for key, value in other_params.iteritems():
            url += _as_param(key, unicode(value))
        url += _as_param('api_key', self._api_key)
        return url
        
    def _tuples_to_params(self, tuples):
        return dict(filter(lambda (k,v): v is not None, tuples))
        
    class LastfmApi:
        
        def __init__(self, lastfm):
            self._lastfm = lastfm
    
    class Geo(LastfmApi):
        """
            Functionality from the Geo methods from the Last.fm API.
        """
        
        def get_events(self, longitude=None, latitude=None, location=None, distance=None, page=None, tag=None, festivalsonly=None, limit=None):
            return self._lastfm.get('geo.getevents', self._lastfm._tuples_to_params([('long', longitude), ('lat', latitude), ('location', location), ('distance', distance), ('page', page), ('tag', tag), ('festivalsonly', festivalsonly), ('limit', limit)]))
            
        def get_top_artists(self, metro, country, start=None, end=None, page=None, limit=None):
            if not metro or not country:
                raise ValueError("'Metro' and 'Country' need to be informed.")
            return self._lastfm.get('geo.gettopartists', self._lastfm._tuples_to_params([('metro', metro), ('country', country), ('start', start), ('end', end), ('page', page), ('limit', limit)]))
            
    class Venue(LastfmApi):
        """
            Functionality from the Venue methods from the Last.fm API.
        """
        
    class Artist(LastfmApi):
        """
            Functionality from the Artist methods from the Last.fm API.
        """
    
    class Event(LastfmApi):
        """
            Functionality from the Event methods from the Last.fm API.
        """
        