# Import of the required modules
from microbit import *

# Servo control
# 100 = 1 millisecond pulse all the way to the right (0°)
# 150 = 1.5 milliseconds pulse centered (90°)
# 200 = 2 milliseconds pulse on the far left (180°)

# PWM period time setting
pin1.set_analog_period(10)
pin13.set_analog_period(10)

# The scale function is used to convert the input
# values (0-180°) to 100 - 200 (1 ms - 2 ms)
def scale(num, in_min, in_max, out_min, out_max):
    # Return of the value rounded to a whole number
    return (round((num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min))

# The servo function controls servo channel 1 or 2
# (x) to a position between 0 and 180 (y)
def servo(x, y):
    # Channel query with plausibility check of the transferred values x and y
    if x == 1 and y >= 0 and y <= 180:
        # Pin 1 (servo channel 1) Scale and adjust PWM signal according to angle y
        pin1.write_analog(scale(y, 0, 180, 100, 200))
    elif x == 2 and y >= 0 and y <= 180:
        # Pin 2 (servo channel 2) Scale and adjust PWM signal according to angle y
        pin13.write_analog(scale(y, 0, 180, 100, 200))
    else:
        # if none of the situations defined above apply
        print("error")

while True:
    servo(1, 0)  # Channel 1 0° (far right)
    servo(2, 180)  # Channel 2 180° (far left)
    sleep(2000)  # 2 seconds pause
    servo(1, 180)  # Channel 1 180° (far left)
    servo(2, 0)  # Channel 2 0 ° (far right)
    sleep(2000)  # 2 seconds pause
