# Import of the micro:bit module
from microbit import *

# Initialization of the I2C interface
i2c.init(freq=400000, sda=pin20, scl=pin19)

# Initialization of the PWM controller
i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')

# The deceleration of a motor can compensate for a different
# speed of the motors due to production-related tolerances.
biasR = 0  # Deceleration of the right motor in percent
biasL = 0  # Deceleration of the left motor in percent

# The scale function is used to rescale the bias
# variables for the calculation of the motor speed.
def scale(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Control motors using the PWM controller
# PWM0 and PWM1 for the left motor and PWM2 and PWM3 for the right motor
def drive(PWM0, PWM1, PWM2, PWM3):
    # Scaling of the deceleration value into the value in percent
    # with which the motor should rotate.
    # Ex: bias = 5 is converted to 95
    # and then divided by 100. 255 * (95/100).
    PWM0 = int(PWM0 * (scale(biasR, 0, 100, 100, 0) / 100))
    # Repeat the procedure for all 4 channels
    PWM1 = int(PWM1 * (scale(biasR, 0, 100, 100, 0) / 100))
    PWM2 = int(PWM2 * (scale(biasL, 0, 100, 100, 0) / 100))
    PWM3 = int(PWM3 * (scale(biasL, 0, 100, 100, 0) / 100))
    # Transfer value for PWM channel (0-255) to PWM controller.
    # 0x70 is the I2C address of the controller. b'\x02 is
    # the byte for PWM channel 1. The byte with the PWM value
    # is added to the byte for the channel.
    i2c.write(0x70, b'\x02' + bytes([PWM0]))
    # Repeat the procedure for all 4 channels
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
            print("backwards")
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

    # Drive left
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

    # Drive right
    elif direction == "r":
        speed += 1
        drive(speed, 0, 0, speed)
        sleep(30)
        if speed > 254:
            stop()
            print("forward")
            sleep(1000)
            speed = 35
            direction = "f"

    # else stop
    else:
        stop()
        print("stopped")
