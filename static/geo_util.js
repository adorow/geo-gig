/**
 * Geolocalization utility.
 * author: andersondorow@gmail.com
 */

function getGeoPos(success, failure) {
    if (navigator && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, failure);
    } else {
        failure('geolocation not supported');
    }
}