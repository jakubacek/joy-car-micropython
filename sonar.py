# Import of the required modules
from microbit import *
from machine import time_pulse_us
import gc

# Define pins
trigger = pin8
echo = pin12

# Initialization of the pins
trigger.write_digital(0)
echo.read_digital()

# definition of the function get_distance, which performs the distance measurement
def get_distance():
    gc.disable()  # Disable garbage collector
    trigger.write_digital(1)  # Send short pulse on the trigger pin of the sensor
    trigger.write_digital(0)  # End pulse on the trigger pin

    stopwatch = time_pulse_us(echo, 1)  # Time measurement until the echo pin is set high
    duration = stopwatch / 1000000  # Conversion in seconds
    distance = (duration * 34300) / 2  # Calculation of the distance

    return round(distance, 2)  # Return distance rounded to 2 decimal places

while True:
    print(get_distance())  # Execute and output the distance function
    sleep(500)
