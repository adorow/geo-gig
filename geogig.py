
import logging
import webapp2
import jinja2
import os

from geogig_format_util import get_coordinate_from_event
from lastfm_little_wrapper import Lastfm
from html_text_builder import HtmlTextBuilder
from num_util import parse_num
from gig_searcher import *
from lastfm_gig_searcher import *
from itertools_plus import group_by

LASTFM_API_KEY = "9b6deef6cb410837dd90c9a15fa1a4cf"

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class BaseRequestHandler(webapp2.RequestHandler):
    "Base Request Handler implementation, with some useful functions."
    
    def _get_param(self, param):
        "Obtains a parameter from the request."
        return self.request.get(param)
    
    def _get_error(self, title, description = None, help = None):
        "Writes an error page with a given error."
        html = HtmlTextBuilder().text(title)
        if description:
            html.linebreak(2).text(description)
        if help:
            html.linebreak(2).text(help)
        
        return self._get_message(html)
    
    def _get_message(self, html):
        "Writes a page with a message."
        self._write('message.html', {'message': html})
        
    def _write(self, template, values={}):
        "Writes a page defined by the given template, and with the values informed."
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

    @staticmethod
    def _get_latitude_and_longitude_from_query(q):
        "Tries to parse the query as two numbers, if is not possible to get exactly that, return two None values."
        nums = map(parse_num, q.split())
        if len(nums) != 2 or not all(nums):
            return (None, None)
        return map(str, nums) # they have to be strings
            
    def get(self):
        q = self._get_param('q')
        logging.debug('Query received: "' + q + '".')
        lat, lon = self._get_latitude_and_longitude_from_query(q)
        
        try:
            gig_searcher = GigSearcher(LastfmGigSearcherSource(LASTFM_API_KEY), LastfmGigSearchResultTranslator())
            if (lat and lon):
                events_list = gig_searcher.search_by_coordinates(lat, lon)
            else:
                events_list = gig_searcher.search_by_location(q)
                
                # get all the points of the events
                points = map(lambda e: map(parse_num, get_coordinate_from_event(e)), events_list) 
                sum_lat, sum_lon = reduce(lambda (lat1, lon1), (lat2, lon2): (lat1 + lat2, lon1 + lon2), points, (0,0))
                # get the average latitude and longitude
                lat, lon = (str(sum_lat / len(points)), str(sum_lon / len(points))) if len(points) > 0 else (0,0)

            events_list = group_by(events_list, key=get_coordinate_from_event)
                
            self._write('search.html', { 'center': {'latitude': lat, 'longitude': lon }, 'zoom': 8, 'events': events_list.items() })
        except GigSearchException as e:
            logging.error('Error on search for query "' + q + '". Description: ' + e.strerror)
            self._get_error('Error requesting to the service ' + e.service + ' for query "' + q + '".', description=e.strerror)
        except IOError as e:
            logging.error('Unexpected error rouse while querying for "' + q + '". Description: ' + str(e))
            self._get_error('Something suddenly went wrong when you queried for "' + q + '", try again later.', description=str(e))

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
