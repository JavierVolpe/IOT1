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


import umqtt_robust2 as mqtt
from machine import Pin, ADC, UART
from time import sleep
from gps_bare_minimum import GPS_Minimum # Vi bruger GPS functioner, som vi har fået af Kevin

YELLOW_PIN = 15  # PIN nummer til GRØN led - requires bridge in port expander
led1 = Pin(
    YELLOW_PIN, Pin.OUT
)  # bruger modul PIN for at sende signal OUT til LED


#########################################################################
# CONFIGURATION
gps_port = 2  # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600  # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)  # UART object creation
gps = GPS_Minimum(uart)  # GPS object creation


# Battery voltage function (Fra Bo)
bat_adc = ADC(Pin(35))  # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)  # Full range: 3,3 V

# Battery
pin_adc_bat = 35  # The battery status input pin
bat_scaling = 4.2 / 3413  # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied

send_battery = 1  # Hvis 1, så sender battery percentage til AdafruitGPS Function



#   Reads the battery from a converted ADC value
#   Input : none
#   Output: the battery voltage
# 	Kilde: Bo Hansen
def read_battery_voltage_avg64():  # Option: average over N times to remove fluctuations
    adc_val = 0
    for i in range(64):
        adc_val += bat_adc.read()
    voltage = bat_scaling * (adc_val >> 6)  # >> fast divide by 64
    return voltage



# Kilde: Kevin L.
def get_adafruit_gps():
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
            return speed + "," + lat + "," + lon + "," + "0.0"
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
        gps_data = get_adafruit_gps()
        if gps_data:  # hvis der er korrekt data så send til adafruit
            print(f"\ngps_data er: {gps_data}")  # Viser GPS data
            mqtt.web_print(
                gps_data, "JavierVo/feeds/mapfeed/csv"
            )  # Besked til Adafruit med gps data, til feed mapfeed
            sleep(4)
#         else:
#             print(
#                 "No GPS Data"
#             )  # Hvis vi ikke har fået gyldig data, viser vi det på shell

        # Opdatering af batteriniveau til Adafruit i feed "batteryfeed"
        if send_battery == 1:  # Sender batteriniveau KUN hvis vi aktivere den
            battery_percent = round(read_battery_voltage_avg64() / 4.2 * 100, 2)
            if battery_percent > 100:
                print("Error: Battery over 100%")
            elif battery_percent < 0:
                print("Error: Battery under 0%")
            else:
                print(battery_percent)  # Viser det på shell 
                mqtt.web_print(
                    battery_percent, "JavierVo/feeds/batteryfeed"
                )   # opdatere feed til Adafruit
        led1.on()   # YELLOW LED Blink
        sleep(2.5)  # Venter 2x2.5 sek. (begrænse af Adafruit til at modtage beskeder)
        led1.off()  # YELLOW LED Blink
        sleep(2.5)
        if len(mqtt.besked) != 0:  # Her nulstilles indkommende beskeder
            mqtt.besked = ""
        mqtt.sync_with_adafruitIO()  # igangsæt at sende og modtage data med Adafruit IO
        print(".", end="")  # printer et punktum til shell, uden et enter

    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print("Ctrl-C pressed...exiting")
        mqtt.c.disconnect()
        mqtt.sys.exit()

