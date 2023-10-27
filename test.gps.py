# import math
from math import radians, cos, sin, asin, sqrt
import time

from machine import UART
from gps_bare_minimum import GPS_Minimum #Vi bruger GPS functioner, som vi har fået af Kevin
# #########################################################################
# # CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
# #########################################################################
# # OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation





#Haversine formula kilde: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r





# Continuous loop for measuring and printing the distance
while True:
    # Replace these with actual GPS readings
    lat1 = 52.5200
    lon1 = 13.4050
    lat2 = 48.8566
    lon2 = 2.3522

    # Calculate the distance using the haversine function
    distance = haversine(lat1, lon1, lat2, lon2)
    print("Distance:", distance, "km")

    # Read the next set of GPS coordinates here
    # lat1, lon1 = read_gps_coordinates()  # Replace with your GPS reading code

    # Wait for 2 seconds before the next GPS update
    time.sleep(2)
