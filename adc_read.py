# Import of the micro:bit module
from microbit import *

# Variables needed for conversion 3.3 V / 1024
# (max. voltage at ADC pin / ADC resolution)
uref = 0.00322265625
# (10 kOhm + 5,6 kOhm) / 5,6 kOhm [(R1 + R2) / R2, Voltage divider ratio]
uratio = 2.7857142

def supplyVoltage():
    adcvoltage = pin2.read_analog()  # Reading the ADC value
    voltaged = uref * adcvoltage  # Convert ADC value to volts
    # Multiply measured voltage by voltage divider ratio to calculate actual voltage
    voltagep = voltaged * uratio
    return voltagep  # returns the variable voltagep

# Demo-Loop
while True:
    # executes the function supplyVoltage and stores the return in sup_volt
    sup_volt = supplyVoltage()
    # Outputs the value from sup_volt formatted with text
    print("Input voltage = " + str(sup_volt) + " V")
    sleep(2000)
