# Import of the micro:bit module
from microbit import *

# Initialization of the I2C interface
i2c.init(freq=400000, sda=pin20, scl=pin19)

# sets the additional output 7 of the IO Expander low
def out7off():
    i2c.write(0x38, b'\x7f')

# sets the additional output of the IO Expander high
def out7on():
    i2c.write(0x38, b'\xff')

# Demo-Loop
while True:
    out7off()
    sleep(1000)
    out7on()
    sleep(1000)
