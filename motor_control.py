# Import of the micro:bit module
from microbit import *

# Initialization of the I2C interface
i2c.init(freq=400000, sda=pin20, scl=pin19)

# Initialization of the PWM controller
i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')

# Controlling motors using the PWM controller
# PWM0 and PWM1 for the left motor and PWM2 and PWM3 for the right motor
def drive(PWM0, PWM1, PWM2, PWM3):
    # Transfer value for PWM channel (0-255) to PWM controller.
    # 0x70 is the I2C address of the controller.
    # b'\x02 is the byte for PWM channel 1.
    # The byte with the PWM value is added to the byte for the channel.
    i2c.write(0x70, b'\x02' + bytes([PWM0]))
    # Repeat the process for all 4 channels
    i2c.write(0x70, b'\x03' + bytes([PWM1]))
    i2c.write(0x70, b'\x04' + bytes([PWM2]))
    i2c.write(0x70, b'\x05' + bytes([PWM3]))

# stop all motors
def stop():
    drive(0, 0, 0, 0)


# Variables for the demo-while loop
speed = 35
direction = "f"

# Demo-loop
while True:

    # drive forward
    if direction == "f":
        speed += 1
        drive(speed, 0, speed, 0)
        sleep(30)
        if speed > 254:
            stop()
            print("reverse")
            sleep(1000)
            speed = 35
            direction = "b"

    # reverse
    elif direction == "b":
        speed += 1
        drive(0, speed, 0, speed)
        sleep(30)
        if speed > 254:
            stop()
            print("left")
            sleep(1000)
            speed = 35
            direction = "l"

    # Turn left
    elif direction == "l":
        speed += 1
        drive(0, speed, speed, 0)
        sleep(30)
        if speed > 254:
            stop()
            print("right")
            sleep(1000)
            speed = 35
            direction = "r"

    # Turn right
    elif direction == "r":
        speed += 1
        drive(speed, 0, 0, speed)
        sleep(30)
        if speed > 254:
            stop()
            print("forwards")
            sleep(1000)
            speed = 35
            direction = "f"

    # else stop
    else:
        stop()
        print("stopped")
