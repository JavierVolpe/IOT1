# Gruppe 4, IT-TEK 1B e023

# Emil Fabricius Schlosser
# Javier Alejandro Volpe
# Jonathan Steenstrup
# Morten Hamborg Johansen

#########################################################################
# DEPENDENCIES
import umqtt_robust2 as mqtt 					# MQTT til at sende beskeder til Adafruit
from machine import Pin, ADC, UART, PWM, I2C 	# Hardware moduler
from time import sleep							# Sleep funktion
from gps_bare_minimum import GPS_Minimum 		# GPS functioner af Kevin Lindemark 
from math import radians, sin, cos, sqrt, asin 	# Moduler til Haversine formel 
from mpu6050 import MPU6050						# IMU sensor MPU6050
import _thread									# Multi-threading support

#########################################################################
# CONFIGURATION HARDWARE
YELLOW_PIN 	= 15  	# PIN nummer til yellow LED - for at vise at programmet kører
BUZZ_PIN 	= 33 	# Buzzer PIN
gps_port 	= 2    			# ESP32 UART port, Educaboard ESP32 default UART port
gps_speed 	= 9600    		# UART speed, defauls u-blox speed

#########################################################################
# CONFIGURATION PROGRAM
# Battery
pin_adc_bat = 35  			# The battery status input pin
bat_scaling = 4.2 / 3413  	# The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

# Opdatering til Adafruit 
send_battery 		= 1		# Hvis 1: sender batteri percentage til Adafruit
send_location_data 	= 1 	# Hvis 1: sender lokation opdatering til Adafruit
send_distance 		= 1 	# Hvis 1: sender distancer til Adafruit. 
send_taklinger 		= 1 	# Hvis 1: sender antal af taklinger

# Adafruit feeds config:
distance_km_feed	= "JavierVo/feeds/distancekm"
map_feed 			= "JavierVo/feeds/mapfeed/csv"
battery_feed 		= "JavierVo/feeds/batteryfeed"
taklinger_feed 		= "JavierVo/feeds/taklinger"

#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           	# UART object creation
gps = GPS_Minimum(uart)                    	# GPS object creation
led1 = Pin(YELLOW_PIN, Pin.OUT)  			# bruger modul PIN for at sende signal OUT til Pin 15
buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT)) 		# Initialiserer PWM modul til buzzer 
buzzer.duty(0) 								# Mute at start
bat_adc = ADC(Pin(pin_adc_bat)) 			# The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)  				# Full range: 3,3 V
i2c = I2C(0) 								# I2C objekt
imu = MPU6050(i2c)							# IMU: MPU6050 objekt

#########################################################################
# EMPTY VARIABLES AT START
coordinates 		= [] 	# Start uden koordinater
kmcount 			= 0 	# Starter med 0 km
taklinger 			= 0		# 
reported_taklinger 	= 0
distance 			= 0
#########################################################################
# FUNCTIONS
# # Distance / koordinater
# Haversine funktion(Michael Dunn) kilde: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
# Modificeret til at bruge meter
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 # Radius of earth in meters. 
    return c * r

def total_distance(coordinates):
    # Total distance. 
    # Først bruger det parse_coord() til at transformere strings til en liste af lister.
    # Så tager det hver element i listen, og beregne distance til den næste element, ved at bruge
    # Haversine funktion. Returnerer distance mellem ALLE koordinater. 
    total = 0 #Starts med 0 km
    coordinates = parse_coord(coordinates)
    for i in range(len(coordinates) - 1): # Loop til hver koordinatpar
        lat1, lon1 = coordinates[i]
        lat2, lon2 = coordinates[i + 1]
        total += haversine(lat1, lon1, lat2, lon2)
    return total #Total i MT

def parse_coord(coordinates): 
    # parse_coord:
    # Transformere en list af strings med koordinater, adskilt af et komma, til en liste af lister,
    # hvor hvert koordinatpar er opdelt i to elementer (latitude og longitude), og hvor komma er fjernet.
    # Eksempel:
    #     Input: ['55.69186,12.55446', '55.69185,12.55443', '55.19185,12.35443']
    #     Output: [['55.69186', '12.55446'], ['55.69185', '12.55443'], ['55.19185', '12.35443']]
    newcoord = []
    for item in coordinates:
        split = item.split(",") # split on commas in string
        newcoord.append([float(split[1]),float(split[2])]) # Hver element i en list, er en list af koordinater. Elementer 1 og 2 er lat / long. 
    return newcoord # Returnere en list af koordinater

def read_battery_voltage_avg64():  # Option: average over N times to remove fluctuations
    # Batteri funktion:
    # Reads the battery from a converted ADC value
    # Input : none
    # Output: the battery voltage
    # Kilde: Bo Hansen / Undervisning ILS 1/08
    adc_val = 0
    for i in range(64):
        adc_val += bat_adc.read()
    voltage = bat_scaling * (adc_val >> 6)  # >> fast divide by 64
    return voltage


def get_adafruit_gps():
    # Læser GPS lokation til Adafruit:
    # Kilde: Kevin Lindemark 
    speed = lat = lon = None  # Opretter variabler med None som værdi
    if gps.receive_nmea_data():
        # hvis der er kommet end bruggbar værdi på alle der skal anvendes
        if (
            gps.get_speed() != -999
            and gps.get_latitude() != -999.0
            and gps.get_longitude() != -999.0
            and gps.get_validity() == "A"
        ):
            # gemmer returværdier fra metodekald i variabler
            speed = str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0"
           
        else:  # hvis ikke både hastighed, latitude og longtitude er korrekte
            print(
                f"Invalid GPS data: \nspeed: {speed} / latitude: {lat} / longtitude: {lon}"
            )
            print()
            return False
    else:
        return False
    
def spill_lyd():
    buzzer.duty(512) 
    buzzer.freq(500)
    sleep(0.2)
    buzzer.duty(0)

def taklinger_counter(): 
    # Kører i anden thread
    # Hvis acceleration Z stiger over 31000 eller falder under -31000, viser det på shell,
    # og tæller op i globale variabel "taklinger" 
    global taklinger
    if not taklinger:
        taklinger = 0
    state = 0
    from mpu6050 import MPU6050
    from machine import I2C
    while True:
        try:   
            imu_data = imu.get_values()
            imudata = imu_data.get("acceleration z")
            sleep(0.01)
            if  imudata <= -31000 or imudata >= 31000 and state == 0:
                    print(imudata)
                    taklinger += 1
                    state = 1
                    print(taklinger)
                    sleep(2)
            elif imudata >= -10000 or imudata <= 10000 and state == 1:
                state = 0
        except:
            print("Warning: Missing connection to IMU. ")
            continue 
            
# # # Program
_thread.start_new_thread(taklinger_counter, ()) #Starter tackling detektion funktion i nyt thread

while True:
    try:
        #ID 6: Taklinger
        if taklinger != reported_taklinger and send_taklinger == 1: #Tjekker om der er flere taklinger end sidste sendt til Adafruit
            mqtt.web_print(taklinger, taklinger_feed) #Informere Adafruit on antal taklinger
            print("Sende tacklinger: ", taklinger)
            reported_taklinger = taklinger
            sleep(4)
        
        #ID 8: Distance måling
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_data = get_adafruit_gps()
        sleep(1)
        if gps_data: 
            coordinates.append(gps_data) #Tilføjer koordinater til listen "coordinates"
            
            #ID 1: Lokation til Adafruit kort
            print(f"\nLokation til Adafruit kort: {gps_data} (lat, long)")  # Viser GPS data
            if send_location_data == 1:
                mqtt.web_print(gps_data, map_feed)  # Besked til Adafruit med gps data, til feed map_feed
                sleep(4)
                

        if len(coordinates) > 1: #Når der er flere koordinater i listen, beregner det distancen
            print(f"Beregner distance {len(coordinates)} koordinater: {coordinates}")
            
        distance = round(total_distance(coordinates), 4) #TODO: kun 2 decimaler.
                    
        if distance > 10 and distance < 1000 and kmcount == 0:
            print ("Distance over 100 meters. Distance: ", distance, "meters.")
            if send_distance == 1:
                distance_km = distance / 1000
                mqtt.web_print(distance_km, distance_km_feed) #Feed distance
                print("Informing distance:", distance, "meters.")
                sleep(4)
                
        if distance >= 1000: 
            print("Distance over 1 km. Spiller lyd og informere AF. Distance: ", distance)
            spill_lyd()
            if send_distance == 1:
                mqtt.web_print(kmcount, distance_km_feed) # Distance i KM til feed kmcount
                print("Informing distance", distance)
                sleep(4)
            
            kmcount = kmcount + (distance / 1000)
            distance = 0
            coordinates.clear() 
            
        if kmcount != 0:
            #Når vi har løbet over 1km men mindre en 999 mt over.
            kmcount = kmcount + (distance / 1000)
            if kmcount > 1:
                print("Distance km: ", kmcount)
            if send_distance == 1:
                mqtt.web_print(kmcount, distance_km_feed) # Distance i KM til feed kmcount
                sleep(4)
                print("Informing distance", kmcount)
                    
            print("Distance meters: ", kmcount * 1000)
            distance = 0
            
        if len(coordinates) > 4: #Maks. 4 koordinater af gang, pga. mangel af memory i ESP32
            kmcount =  distance / 1000 + kmcount
            print("Clear koordinater. Distance: ", kmcount, "km.")
            coordinates.clear()
            coordinates = []
            

        # ID 1
        # Opdatering af batteriniveau til Adafruit i feed "batteryfeed"
        if send_battery == 1:  # Config            
            battery_voltage = round(read_battery_voltage_avg64(), 2) # 
            battery_percent = round(battery_voltage / 4.2 * 100, 2) #Beregner batteri niveau ud fra ADC værdi / maks. spændning
            if battery_percent > 100:
                print("Error: Battery over 100%")
            elif battery_percent < 0:
                print("Error: Battery under 0%")
            else:
                print(f"Batteri niveau: {battery_percent} % / {battery_voltage} v")  # Viser det på shell 
                mqtt.web_print(battery_percent, battery_feed) # Sender besked til Adafruit med batteri niveau 
                sleep(4)
                
        if len(mqtt.besked) != 0: 	# Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(" ", end = '') 		# printer et punktum til shell, uden et enter        

    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()
