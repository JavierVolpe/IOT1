# Python dictionary {} der indeholder login oplysninger
# Undlad at uploade denne fil til github når den er udfyldt

# ADAFRUIT_IO_URL behøves ikke at ændres

# ADAFRUIT_IO_FEEDNAME behøves ikke at ændres (men skal oprettes med samme navn)
# men der skal oprettes en feed med samme navn på adafruit.io

location = "Kea" # "Kea", "Hjem", "Hotspot"

if location == "Kea":
    credentials = {
    'ssid' : 'KEA_Starlink',
    'password' : '',  
    'ADAFRUIT_IO_URL' : b'io.adafruit.com',
    'ADAFRUIT_USERNAME' : b'',
    'ADAFRUIT_IO_KEY' : b'aio_',
    'ADAFRUIT_IO_FEEDNAME' : b'batteryfeed'
    }
elif location == "Hjem":
    credentials = {
    'ssid' : 'Jwifi',
    'password' : '',
    'ADAFRUIT_IO_URL' : b'io.adafruit.com',
    'ADAFRUIT_USERNAME' : b'',
    'ADAFRUIT_IO_KEY' : b'aio_',
    'ADAFRUIT_IO_FEEDNAME' : b'speed'
    }
elif location == "Hotspot":
    credentials = {
    'ssid' : 'iPhoneJV',
    'password' : '',    
    'ADAFRUIT_IO_URL' : b'io.adafruit.com',
    'ADAFRUIT_USERNAME' : b'',
    'ADAFRUIT_IO_KEY' : b'aio_',
    'ADAFRUIT_IO_FEEDNAME' : b'ESP32feed'
    }
else:
    credentials = {
    'ssid' : '',
    'password' : '',    
    'ADAFRUIT_IO_URL' : b'io.adafruit.com',
    'ADAFRUIT_USERNAME' : b'',
    'ADAFRUIT_IO_KEY' : b'aio_',
    'ADAFRUIT_IO_FEEDNAME' : b'ESP32feed'
    }
    
    