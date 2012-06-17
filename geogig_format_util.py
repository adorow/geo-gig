# This file contains functions that are useful to treat information in the geogig format (defined in geogig-search-result-format.txt). 

def get_coordinate_from_event(event):
    "Obtains a tuple with the coordinates (latitude, longitude) of an event."
    coord = event['venue']['location']['coordinates']
    return (coord['latitude'], coord['longitude'])
    
def validate_event(event):
    "Validates the event structure. Calling this function, is guaranteed that, if no errors occur, the event is perfectly structured, following the guidelines defined in geogig-search-result-format.txt."

    if 'title' not in event:
        raise ValueError('title missing')
    
    if 'image_url' not in event:
        raise ValueError('image_url missing')
    
    if 'url' not in event:
        raise ValueError('url missing')
    
    if 'cancelled' not in event:
        raise ValueError('cancelled missing')
        
    if 'date' not in event:
        raise ValueError('date missing')
    
    if 'artists' not in event:
        raise ValueError('artists missing')
    
    if 'venue' not in event:
        raise ValueError('venue missing')
        
    for artist in event['artists']:
        validate_artist(artist)
        
    validate_venue(event['venue'])
    
def validate_venue(venue):
    "Validates the venue structure. Calling this function, is guaranteed that, if no errors occur, the venue is perfectly structured, following the guidelines defined in geogig-search-result-format.txt."
    
    if 'name' not in event:
        raise ValueError('name missing')
    
    if 'phonenumber' not in event:
        raise ValueError('phonenumber missing')
    
    if 'url' not in event:
        raise ValueError('url missing')
    
    if 'location' not in event:
        raise ValueError('location missing')
    
    validate_location(event['location'])

def validate_location(location):
    "Validates the location structure. Calling this function, is guaranteed that, if no errors occur, the location is perfectly structured, following the guidelines defined in geogig-search-result-format.txt."
    
    if 'street' not in event:
        raise ValueError('street missing')
    
    if 'postalcode' not in event:
        raise ValueError('postalcode missing')
    
    if 'city' not in event:
        raise ValueError('city missing')
    
    if 'country' not in event:
        raise ValueError('country missing')
    
    if 'coordinates' not in event:
        raise ValueError('coordinates missing')
    
    validate_cordinates(event['coordinates'])
    
def validate_artist(artist):
    "Validates the artist structure. Calling this function, is guaranteed that, if no errors occur, the artist is perfectly structured, following the guidelines defined in geogig-search-result-format.txt."
   
    if 'name' not in event:
        raise ValueError('name missing')
        
    if 'url' not in event:
        raise ValueError('url missing')
    

def validate_coordinates(coordinates):
    "Validates the coordinates structure. Calling this function, is guaranteed that, if no errors occur, the coordinates is perfectly structured, following the guidelines defined in geogig-search-result-format.txt."
    
    if 'latitude' not in event:
        raise ValueError('latitude missing')
        
    if 'longitude' not in event:
        raise ValueError('longitude missing')
    