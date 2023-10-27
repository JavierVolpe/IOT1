from machine import Pin, ADC
from time import sleep

def read_battery():
    adc = ADC(Pin(35)) # # ADC Pin til at læse batteri niveau (Vi bruger PIN 32 og ikke 25 fordi 25 er forbyndet til ADC1, og vi kan ikke bruge det samtidigt at vi bruger wifi. Derfor bruger vi 32, som er ADC2
    adc.atten(ADC.ATTN_11DB)
    values = adc.read()
    
    # vmax = 4.2
    # vmin = 3.7
    
#     percent = 4.2 / values
    percent = values
    
#     battery_percent = round(values / 40.95, 2)
    return percent

while True:
    print (read_battery())
    sleep(1)