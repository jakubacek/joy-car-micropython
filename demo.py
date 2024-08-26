from microbit import *
import neopixel
import gc

np = neopixel.NeoPixel(pin0, 8)
headlights = (0, 3)
backlights = (5, 6)
led_white = (60, 60, 60)
led_red = (60, 0, 0)
led_off = (0, 0, 0)
led_red_br = (255, 0, 0)
led_orange = (100, 35, 0)
indicator_left = (1, 4)
indicator_right = (2, 7)
indicator_warning = (1, 2, 4, 7)
i2c.init(freq=400000, sda=pin20, scl=pin19)

i2c.write(0x70, b'\x00\x01')
i2c.write(0x70, b'\xE8\xAA')

mode = 0

def zfill(s, width):
    return '{:0>{w}}'.format(s, w=width)

def fetchSensorData():
    data = "{0:b}".format(ord(i2c.read(0x38, 1)))
    data = zfill(data, 8)

    bol_data_dict = {}
    bit_count = 7

    for i in data:
        if i == "0":
            bol_data_dict[bit_count] = False
            bit_count -= 1
        else:
            bol_data_dict[bit_count] = True
            bit_count -= 1
    return bol_data_dict
    # bit 0 = SpeedLeft, bit 1 = SpeedRight, bit 2 = LineTrackerLeft,
    # bit 3 = LineTrackerMiddle, bit 4 = LineTrackerRight,
    # bit 5 = ObstclLeft, bit 6 = ObstclRight, bit 7 = Buzzer
def drive(PWM0, PWM1, PWM2, PWM3):
    i2c.write(0x70, b'\x02' + PWM0)
    i2c.write(0x70, b'\x03' + PWM1)
    i2c.write(0x70, b'\x04' + PWM2)
    i2c.write(0x70, b'\x05' + PWM3)

def lightsON():
    for x in headlights:
        np[x] = led_white
    for x in backlights:
        np[x] = led_red
    np.show()

def lightsOFF():
    for x in headlights:
        np[x] = led_off
    for x in backlights:
        np[x] = led_off
    np.show()

for x in range(0, 8):
    np[x] = (255, 0, 0)
np.show()
sleep(400)
for x in range(0, 8):
    np[x] = (0, 255, 0)
np.show()
sleep(400)
for x in range(0, 8):
    np[x] = (0, 0, 255)
np.show()
sleep(400)
for x in range(0, 8):
    np[x] = (0, 255, 0)
np.show()
sleep(400)
for x in range(0, 8):
    np[x] = (0, 0, 0)
np.show()
sleep(200)

while True:
    if button_a.was_pressed() == 1:
        mode += 1
        if mode > 2:
            mode = 0
    display.show(mode)
    if mode == 0:
        drive(bytes([0]), bytes([0]), bytes([0]), bytes([0]))
        for x in range(0, 8):
            np[x] = (50, 0, 0)
        np.show()
    else:
        for x in range(0, 8):
            np[x] = (0, 0, 0)
        np.show()
    if mode == 1:
        sen_data = fetchSensorData()
        if sen_data[2] is False and sen_data[3] is False and sen_data[4] is True:
            drive(bytes([0]), bytes([0]), bytes([60]), bytes([255]))
        elif sen_data[2] is False and sen_data[3] is True and sen_data[4] is True:
            drive(bytes([60]), bytes([255]), bytes([30]), bytes([255]))
        elif sen_data[2] is True and sen_data[3] is False and sen_data[4] is False:
            drive(bytes([60]), bytes([255]), bytes([0]), bytes([0]))
        elif sen_data[2] is True and sen_data[3] is False and sen_data[4] is True:
            drive(bytes([0]), bytes([0]), bytes([0]), bytes([0]))
        elif sen_data[2] is True and sen_data[3] is True and sen_data[4] is False:
            drive(bytes([30]), bytes([255]), bytes([60]), bytes([255]))
        else:
            drive(bytes([60]), bytes([255]), bytes([60]), bytes([255]))
    elif mode == 2:
        sen_data = fetchSensorData()
        sleep(3)
        if sen_data[5] is False and sen_data[6] is True:
            # slow back left
            drive(bytes([255]), bytes([40]), bytes([0]), bytes([0]))
            sleep(500)
        elif sen_data[5] is True and sen_data[6] is False:
            # slow back right
            drive(bytes([0]), bytes([0]), bytes([255]), bytes([40]))
            sleep(500)
        elif sen_data[5] is False and sen_data[6] is False:
            drive(bytes([255]), bytes([40]), bytes([40]), bytes([255]))
            sleep(500)
        else:
            drive(bytes([40]), bytes([255]), bytes([40]), bytes([255]))
    gc.collect()
