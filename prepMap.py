import googlemaps
from datetime import datetime, timedelta
import settings

GMAP_API_KEY='AIzaSyDD8nmmHyBYbCvjnFw_bX4cXhZHi_nN65s'
gmaps = googlemaps.Client(key=GMAP_API_KEY)
destAdd="Shaniwarwada Pune"
destination_location = gmaps.geocode(destAdd)
current_location = gmaps.reverse_geocode((settings.gpsLat,settings.gpsLong))

gmaps.distance_matrix(origins=current_location[0]['formatted_address'],destinations=destination_location[0]["formatted_address"],departure_time=datetime.now() + timedelta(minutes=10))

directions_result = gmaps.directions(current_location[0]['formatted_address'], destination_location[0]["formatted_address"], mode="transit", arrival_time=datetime.now() + timedelta(minutes=0.5))

print("directions_result:", directions_result)
locations = [current_location , destination_location ]
markers = ["color:blue|size:mid|label:" + chr(65+i) + "|" + r for i, r in enumerate(locations)]

result_map = gmaps.static_map(center=locations[0],scale=2,zoom=12,size=[640, 640],format="jpg", maptype="roadmap", markers=markers, path="color:0x0000ff|weight:2|" + "|".join(locations))

