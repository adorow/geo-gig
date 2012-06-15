import webapp2

import jinja2
import os

from lastfm_little_wrapper import Lastfm

from html_text_builder import HtmlTextBuilder
from num_util import parse_num

from gig_searcher import *

LASTFM_API_KEY = "9b6deef6cb410837dd90c9a15fa1a4cf"

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class BaseRequestHandler(webapp2.RequestHandler):
    
    def _get_param(self, param):
        return self.request.get(param)
    
    def _get_error(self, title, description = None, help = None):
        html = HtmlTextBuilder().text(title)
        if description:
            html.linebreak(2).text(description)
        if help:
            html.linebreak(2).text(help)
        
        return self._get_message(html)
    
    def _get_message(self, html):
        self._write('message.html', {'message': html})
        
    def _write(self, template, values={}):
        q = self._get_param('q')
        if q:
            values['query'] = q
        self.response.out.write(jinja_environment.get_template(template).render(values))
        

class MainPageHandler(BaseRequestHandler):
    "Handler for the main page."
    def get(self):
        index_message = HtmlTextBuilder().text('Are you looking for gigs?').linebreak(2)
        index_message.text('Write the name of the city and/or country where you want to party, or write a latitude and longitude (in this order), and then press the search button.').linebreak(2)
        index_message.text('Or just press the geolocalized search button, and let geo-gig find the gigs near you.')
        
        self._get_message(index_message)

class GigSearchHandler(BaseRequestHandler):
    "Handler for the search results page."
    def get(self):
        def getLatLon(q):
            nums = map(parse_num, q.split())
            if len(nums) != 2 or not all(nums):
                return (None, None)
            return map(str, nums) # they have to be strings after all
            
        q = self._get_param('q')
        lat, lon = getLatLon(q)
        
        try:
            gig_searcher = LastfmGigSearcher(LASTFM_API_KEY)
            if lat and lon:
                events_list = gig_searcher.searchByCoordinates(lat, lon)
            else:
                events_list = gig_searcher.searchByLocation(q)
                
                # TODO:  there can be places without latitude and longitude (appear as empty strings on the response received), the way it is now, errors occur
                points = map(lambda e: (float(e['venue']['location']['geo:point']['geo:lat']), float(e['venue']['location']['geo:point']['geo:long'])), events_list) # get all the points of the events
                sum_lat, sum_lon = reduce(lambda (lat1, lon1), (lat2, lon2): (lat1 + lat2, lon1 + lon2), points, (0,0))
                lat, lon = (str(sum_lat / len(points)), str(sum_lon / len(points))) if len(points) > 0 else (0,0)
      
            
            self._write('search.html', { 'center': {'latitude': lat, 'longitude': lon }, 'zoom': 8, 'events': events_list })
        except GigSearchException as e:
            self._get_error('Error requesting to the service ' + e.service + ' for query "' + q + '".', description=e.strerror)
        
        # TODO: take a look at the directions webservice https://developers.google.com/maps/documentation/directions/ . Some good ideas may arise. 
        # TODO: the static maps API may be useful some time: https://developers.google.com/maps/documentation/staticmaps
        
        # TODO: for testing purposes, an example of a call to the lastfm api is:
        # http://ws.audioscrobbler.com/2.0/?method=geo.getevents&format=json&latitude=53.366587&longitude=-6.2587435&api_key=9b6deef6cb410837dd90c9a15fa1a4cf
        
        # TODO: try to validate input? to maybe 'throw' a '_get_invalid_search_syntax'?
        #self._get_search(q, lat, lon)
    
    def _get_server_error_on_search(self, service, error, query):
        error_title = 'Error requesting to the service ' + service + ' for query "' + query + '".'
        error_description = HtmlTextBuilder().text('Service responded:').linebreak().text(error).get_text()
        self._get_error(error_title, description=error_description)
    
    def _get_invalid_search_syntax(self, query):
        error_title = 'The query you tried, "' + query + '", is invalid.'
        help_info = HtmlTextBuilder().text('Try queries like').linebreak().text('the name of a city, as in "New York", or "Sao Paulo, Brazil";').linebreak().text('the latitude and longitude of some point in the planet, like "56.02342 -20.48463".')
        
        self._get_error(error_title, help=help_info)
    
app = webapp2.WSGIApplication([('/', MainPageHandler),
                               ('/search', GigSearchHandler)],
                              debug=False)