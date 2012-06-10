import webapp2
import json

import jinja2
import os

from lastfm_little_wrapper import Lastfm


LASTFM_API_KEY = "9b6deef6cb410837dd90c9a15fa1a4cf"
lastfm = Lastfm(LASTFM_API_KEY, 'json')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def get_number(s):
    try:
        return float(s)
    except ValueError:
        return None

class BaseRequestHandler(webapp2.RequestHandler):
     
    def _get_error(self, title, description = None, help = None):
        # TOOD: make it look better, maybe
        html = title
        if description:
            html += '<br /><br />' + description
        if help:
            html += '<br /><br />' + help
        
        return self._get_message(html)
    
    def _get_message(self, html):
        self._write('message.html', {'message': html})
        
    def _write(self, template, values={}):
        q = self.request.get('q')
        if q:
            values['query'] = q
        self.response.out.write(jinja_environment.get_template(template).render(values))
        

class MainPage(BaseRequestHandler):
    def get(self):
        index_message = """
            <span>Are you looking for gigs?</span>
            <BR>
            <BR>
            <span>Write the name of the city and/or country where you want to party, or write a latitude and longitude (in this order), and then press the search button.</span>
            <BR>
            <BR>
            <span>Or just press the geolocalized search button, and let geo-gig find the gigs near you.</span>
        """
        
        self._get_message(index_message)

class GigSearch(BaseRequestHandler):
    def get(self):
        def getLatLon(q):
            nums = map(get_number, q.split())
            if len(nums) != 2 or not all(nums):
                return (None, None)
            return map(str, nums) # they have to be strings after all
            
        q = self.request.get('q')
        lat, lon = getLatLon(q)
        
        # TODO: take a look at the directions webservice https://developers.google.com/maps/documentation/directions/ . Some good ideas may arise.
        # TODO: the static maps API may be useful some time: https://developers.google.com/maps/documentation/staticmaps
        
        # TODO: for testing purposes, an example of a call to the lastfm api is:
        # http://ws.audioscrobbler.com/2.0/?method=geo.getevents&format=json&latitude=53.366587&longitude=-6.2587435&api_key=9b6deef6cb410837dd90c9a15fa1a4cf
        
        # TODO: try to validate input? to maybe 'throw' a '_get_invalid_search_syntax'?
        self._get_search(q, lat, lon)
    
    def _get_server_error_on_search(self, service, error, query):
        error_title = 'Error requesting to the service ' + service + ' for query "' + query + '".'
        error_description = 'Service responded:<br />' + error
        self._get_error(error_title, description=error_description)
    
    def _get_invalid_search_syntax(self, query):
        error_title = 'The query you tried, "' + query + '", is invalid.'
        help_info = """
            Try queries like:<br />
            the name of a city, as in "New York", or "Sao Paulo, Brazil";<br />
            the latitude and longitude of some point in the planet, like "56.02342 -20.48463".
        """
        
        self._get_error(error_title, help=help_info)
    
    def _get_search(self, query=None, latitude=None, longitude=None):
        # TODO: have to make this better. Is very messy (and very ugly. Most of it, at least). A massive refactor is probably on the way... reminder: binsearch idea with distance and limit. 
   
        # location should be sent only if latitude and longitude are not, because when location is informed, the Last.fm API always use this, and ignores latitude and longitude
        lastfm_json_response = lastfm.geo().get_events(location=(query if not (latitude and longitude) else None), latitude=latitude, longitude=longitude, limit=30)
        events_dict = json.loads(lastfm_json_response)
        
        # TODO: the following tells if the response is an error, it needs to be refactored into a method though:
        if 'error' in events_dict:
            self._get_server_error_on_search('Last.fm [Geo.getEvents]', 'Error ' + str(events_dict['error']) + ': ' + events_dict['message'], query)
        else:
            
            # if there's only one event here, it will be the object event, otherwise, it'll be a list of events
            events_list = events_dict['events']['event'] 
            # so, if it's not a list, we make it one
            if not isinstance(events_list, list):
                events_list = [events_list]
            
            if not (latitude and longitude):
                points = map(lambda e: (float(e['venue']['location']['geo:point']['geo:lat']), float(e['venue']['location']['geo:point']['geo:long'])), events_list) # get all the points of the events
                sum_lat, sum_lon = reduce(lambda (lat1, lon1), (lat2, lon2): (lat1 + lat2, lon1 + lon2), points, (0,0))
                latitude, longitude = (str(sum_lat / len(points)), str(sum_lon / len(points))) if len(points) > 0 else (0,0)
            #print events_dict['events']['@attr']  # THIS THING ON THE LEFT SHOWS THE PARAMETERS USED ON THE SEARCH!
            
            self._write('search.html', { 'center': {'latitude': latitude, 'longitude': longitude }, 'zoom': 8, 'events': events_list })
            
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/search', GigSearch)],
                              debug=True)# CHANGE THIS TO 'FALSE' WHEN IT GETS DEPLOYED TO GOOGLEAPPENGINE