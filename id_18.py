# ID: 1
# Kategori:
# UI	Krav:
# Løsningen skal som minimum kunne fremvise lokation og batteridata via et online dashboard, med en opdateringsrate på minimum 2 opdateringer i minuttet.	Prioritet: 1
# Accepttest:
# Step 1) Testbrugeren ifører sig løsningens hardware del, og hardwareløsningen aktiveres.
# Step 2) Indenfor 4 minutter bliver position og batteriniveau data præsenteret i et online dashboard.
# Step 3) Et stopur sættes i gang, og der måles hvor mange opdateringer dashboardet får over en periode på 5 minutter.
#
# Vil der over perioden være 10 eller flere opdateringer, så vurderes kravet som bestået.

# # 
# # ID8  
# # 
# # Kategori: Sensing 
# # 
# # Krav 
# # 
# # Løsningen skal afspille en lyd, hver gang en spiller løber 1kilometer, samt sende optælling af meter til Adafruit, efter de første 100 meter 
# # 
# # Prioritet: 1 
# # 
# # Accepttest:  
# # 
# # Step 1) Testbrugeren ifører sig løsningen hardware del, og hardwareløsningen aktiveres 
# # 
# # Step 2) Testbrugeren bevæger sig 1,1km 
# # 
# # Step 3) Observer om løsningen laver en lyd per kilometer og at dashboardet laver en optælling af meter i et interval af 100meter 
# # 
# #   
# # 
# # Opfyldt 1) 
# # 
# # Hvis løsningen afspiller en lyd indenfor 900 – 1100 meter, og dashboardet laver en optælling indenfor 90-110 meter, er kravet opfyldt 
# # 
# #  
# # 
# # Opfyldt 2)  
# # 
# # Hvis løsningen afspiller en lyd, og dashboardet laver en optælling med en nøjagtighed på +-10%, er kravet opfyldt 


#########################################################################
# DEPENDENCIES
import umqtt_robust2 as mqtt 					# MQTT til at sende beskeder til Adafruit
from machine import Pin, ADC, UART, PWM 		# Hardware moduler
from time import sleep
from gps_bare_minimum import GPS_Minimum 		# GPS functioner af Kevin Lindemark 
from math import radians, sin, cos, sqrt, asin 	# Moduler til Haversine formel 

#########################################################################
# CONFIGURATION HARDWARE
YELLOW_PIN = 15  	# PIN nummer til yellow LED - for at vise at programmet kører
BUZZ_PIN = 33 		# Buzzer PIN
 
#########################################################################
# CONFIGURATION PROGRAM

# GPS
gps_port 	= 2    			# ESP32 UART port, Educaboard ESP32 default UART port
gps_speed 	= 9600    		# UART speed, defauls u-blox speed

# Battery
pin_adc_bat = 35  			# The battery status input pin
bat_scaling = 4.2 / 3413  	# The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

# Opdatering til Adafruit 
send_battery 		= 1		# Hvis 1: sender batteri percentage til Adafruit
send_location_data 	= 1 	# Hvis 1: sender lokation opdatering til Adafruit
send_distance 		= 1 	# Hvis 1: sender distancer til Adafruit. 

# Adafruit feeds config:
distance_feed 	= "JavierVo/feeds/distance"
distance_km_feed= "JavierVo/feeds/distancekm"
map_feed 		= "JavierVo/feeds/mapfeed/csv"
battery_feed 	= "JavierVo/feeds/batteryfeed"


#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           	# UART object creation
gps = GPS_Minimum(uart)                    	# GPS object creation
led1 = Pin(YELLOW_PIN, Pin.OUT)  			# bruger modul PIN for at sende signal OUT til Pin 15
buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT)) 		# Initialiserer PWM modul til buzzer 
buzzer.duty(0) 								# Mute at start

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
    #Total distance. 
    #Først bruger det parse_coord() til at transformere strings til en liste af lister.
    #Så tager det hver element i listen, og beregne distance til den næste element, ved at bruge
    #Haversine funktion. Returnerer distance mellem ALLE koordinater. 
    total = 0 #Starts med 0 km
    coordinates = parse_coord(coordinates)
    for i in range(len(coordinates) - 1): #Loop til hver koordinatpar
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
        newcoord.append([float(split[0]),float(split[1])]) #Hver element i en list, er en list af koordinater
    return newcoord #Returnere en list af koordinater

coordinates = [] 	#Start uden koordinater
kmcount 	= 0 	#Starter med 0 km

# Batteri funktioner:
#   Reads the battery from a converted ADC value
#   Input : none
#   Output: the battery voltage
# 	Kilde: Bo Hansen / Undervisning ILS 1/08

bat_adc = ADC(Pin(pin_adc_bat)) # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)  	# Full range: 3,3 V

def read_battery_voltage_avg64():  # Option: average over N times to remove fluctuations
    adc_val = 0
    for i in range(64):
        adc_val += bat_adc.read()
    voltage = bat_scaling * (adc_val >> 6)  # >> fast divide by 64
    return voltage

# Læser lokation til Adafruit:
# Kilde: Kevin L. - Modificeret til at returnere kun lat + lon, hvis vi skal beregne distancen, ved hjælp af argumenter
def get_adafruit_gps(type_data):
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
            # returnerer data med adafruit gps format
            if type_data == "Location":
                return speed + "," + lat + "," + lon + "," + "0.0"
            elif type_data == "Distance":
                return lat + "," + lon              
                           
        else:  # hvis ikke både hastighed, latitude og longtitude er korrekte
            print(
                f"Invalid GPS data: \nspeed: {speed}\nlatitude: {lat}\nlongtitude: {lon}"
            )
            print()
            return False
    else:
        return False


# # # Program 
while True:
    try:
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_data = get_adafruit_gps("Distance")
        if gps_data: 
            print(f'\nSidste koordinater: {gps_data}') #Viser GPS data i shell 
            coordinates.append(gps_data) #Tilføjer koordinater til list "coordinates"
            led1.off() #Blinker LED når der kommer GPS data. 
            sleep(0.25)
            led1.on()
            sleep(5) #Venter 5 sek.

                
        if len(coordinates) > 1: #Når der er flere koordinater i listen, beregner det distancen
            print(f"Beregner distance mellem koordinater: {coordinates}")
            
            distance = round(total_distance(coordinates), 8) #TODO: kun 2 decimaler.
            print("Løbet distance:", distance, "mt")
 
            if distance > 100: #Over 100 mt.: informere Adafruit
                print(f"Distance over 100: sender besked til adafruit. {distance}")
                if send_distance == 1:
                    mqtt.web_print(distance, distance_feed) #Feed distance
                if kmcount == 0:
                    print(f"Løbet distance: {distance} mt.")
                if kmcount != 0:
                    distance_km_mt = distance * 1000 + kmcount #Distance i mt (gange 1000 til KM) + distance i KM
                    print(f"Løbet KM i alt: {distance_km_mt}")
                sleep(4)

            if distance > 1000: #Distance over 1000: 
                buzzer.duty(512) #Spiller lyd
                buzzer.freq(500)
                sleep(0.2)
                buzzer.duty(0)
                kmcount += (distance / 1000) #Opdaterer km count 
                print(f"Distance over 1000 m. Spiller lyd, sender til adafruit og reset count. Distance i KM: {kmcount}")
                distance = 0 # Reset distance(mt) count
                
                if send_distance == 1:
                    mqtt.web_print(kmcount, distance_km_feed) # Distance i KM til feed kmcount
                    sleep(4)
                coordinates.clear() #Reset list
                
            
        led1.on() # Bruger yellow LED blink til at vise, at programmet kører
        sleep(2)  # (begrænse af Adafruit til at modtage beskeder)
        led1.off()   
        sleep(2)
        
        # Send lokation til Adafruit:
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_location_data = get_adafruit_gps("Location")
        if gps_location_data:  # hvis der er korrekt data så send til adafruit
            print(f"\nLokation til Adafruit kort: {gps_location_data} (speed, lat, long, alt)")  # Viser GPS data
            if send_location_data == 1:
                mqtt.web_print(gps_location_data, map_feed)  # Besked til Adafruit med gps data, til feed mapfeed
                sleep(4)
        
        # Opdatering af batteriniveau til Adafruit i feed "batteryfeed"
        if send_battery == 1:  # Config            
            battery_percent = round(read_battery_voltage_avg64() / 4.2 * 100, 2) #Beregner batteri niveau ud fra ADC værdi / maks. spændning
            if battery_percent > 100:
                print("Error: Battery over 100%")
            elif battery_percent < 0:
                print("Error: Battery under 0%")
            else:
                print(f"Batteri niveau: {battery_percent}")  # Viser det på shell 
                mqtt.web_print(
                    battery_percent, battery_feed
                )   # Sender besked til Adafruit med batteri niveau (i feed batteryfeed)
        led1.on()   # YELLOW LED Blink
        sleep(2.5)  # Venter 2x2.5 sek. (begrænse af Adafruit til at modtage beskeder)
        led1.off()  # YELLOW LED Blink
        sleep(2.5)


        if len(mqtt.besked) != 0: 	# Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') 		# printer et punktum til shell, uden et enter        

    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()


