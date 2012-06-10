geo-gig
=======

The geo-gig is a service where you inform a location, or coordinates of a location, and a map is loaded with information about shows that will be happening near (or at) the given location. It runs on the [Google App Engine][gae] platform. The back-end is built in [Python][py], and the front-end uses [JQuery][jq]. The [Google Maps API][gmaps] is used to build the maps, and the [Last.fm API][lfm] powers the gig search. 

How to use it
-------------

1. Go to [geo-gig][geogig];
2. then type the name of the location (or the coordinates) where you want to look for gigs, or just click the geolocalized search button;
3. a map will appear with all the events found.
4. Enjoy!

Contributing
------------

There are many things you can do to contribute. You can create [issues](https://github.com/adorow/geo-gig/issues) with bug reports, suggestions, or even questions, in case something doesn't look quite right to your eyes. You can review the code as well, and suggest improvements; the code is very messy at this time, as this is the first version (or one of the first few versions, as this text may still be here) and should be heavily refactored soon, so, any suggestion will be welcome. You can improve the interface as well, if you are artistically talented.

[geogig]: http://geo-gig.appspot.com/
[gae]: https://appengine.google.com/
[jq]: http://jquery.com/
[lfm]: http://www.last.fm/
[py]: http://python.org/
[gmaps]: https://developers.google.com/maps/
