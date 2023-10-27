from machine import Pin, ADC
from time import sleep

# Battery voltage function (Fra Bo)
bat_adc = ADC(Pin(35))        # The battery status ADC object
bat_adc.atten(ADC.ATTN_11DB)           # Full range: 3,3 V

# Battery
pin_adc_bat = 35                       # The battery status input pin
bat_scaling = 4.2 / 3413          # The battery voltage divider ratio, replace <adc_4v2> with ADC value when 4,2 V applied


#   Reads the battery from a converted ADC value
#   Input : none
#   Output: the battery voltage
def read_battery_voltage():
    adc_val = bat_adc.read()
    voltage = bat_scaling * adc_val
    return voltage

def read_battery_voltage_avg64():      # Option: average over N times to remove fluctuations
    adc_val = 0
    for i in range(64):
        adc_val += bat_adc.read()      
    voltage = bat_scaling * (adc_val >> 6) # >> fast divide by 64
    return voltage


while True:
    volt = read_battery_voltage_avg64()
    if (volt < 3):
        print("Error: voltage under 3")
    elif (volt > 4.2):
        print ("Error: voltage over 4.2")
    else:
        battery_percent = volt / 4.2 * 100 
        print("Volts: ", volt)
        print("Bat %: ", battery_percent)
        
    print("ADC: ", bat_adc.read())
    print()
#     print (bat_adc.read())
    sleep(1)