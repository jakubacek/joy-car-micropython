# Import of the required modules
from microbit import *
import neopixel
import radio
import music
# Initalization of the RGB LEDs
np = neopixel.NeoPixel(pin0, 8)

# Turn on the radio hardware
radio.on()

# Predefinitions for lighting
headlights = (0, 3)
backlights = (5, 6)
led_white = (60, 60, 60)
led_red = (60, 0, 0)
led_off = (0, 0, 0)

# Function to control the motors
def drive(PWM0, PWM1, PWM2, PWM3):
    i2c.write(0x70, b'\x02' + bytes([PWM0]))
    i2c.write(0x70, b'\x03' + bytes([PWM1]))
    i2c.write(0x70, b'\x04' + bytes([PWM2]))
    i2c.write(0x70, b'\x05' + bytes([PWM3]))

# Switch on low beam
def lightsON():
    for x in headlights:
        np[x] = led_white
    for x in backlights:
        np[x] = led_red
    np.show()

# Switch off light
def lightsOFF():
    for x in headlights:
        np[x] = led_off
    for x in backlights:
        np[x] = led_off
    np.show()


# Control loop
while True:
    # Reception via radio hardware is stored in the variable incoming
    incoming = radio.receive()
    # if incoming is not None (empty) then:
    if incoming is not None:
        # Query the 1st character for the direction
        if incoming[0] == "l":
            drive(0, 0, 40, 255)
        elif incoming[0] == "r":
            drive(40, 255, 0, 0)
        elif incoming[0] == "f":
            drive(40, 255, 40, 255)
        elif incoming[0] == "b":
            drive(255, 40, 255, 40)
        else:
            drive(0, 0, 0, 0)

        # Switching the reversing light on and off
        if incoming[0] == "b":
            np[4] = (led_white)
            np.show()
        else:
            np[4] = (led_off)
            np.show()
        # Query of the 2nd character for the functions (light and horn).
        if incoming[1] == "a":
            music.play("c4:1", pin=pin16)
        elif incoming[1] == "b":
            lightsON()
        elif incoming[1] == "c":
            lightsON()
        else:
            lightsOFF()
    # if incoming = None, then the joy-car is parked.
    # This is usually the case when the joy-car is out of range
    # of the remote control or when the remote control is off.
    else:
        drive(0, 0, 0, 0)
        for x in range(0, 8):
            np[x] = (50, 0, 0)
        np.show()
