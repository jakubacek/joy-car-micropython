# Import of the micro:bit module
from microbit import *

# Initialization of the I2C interface
i2c.init(freq=400000, sda=pin20, scl=pin19)

# Since the function zfill is not included in micro:bit Micropython,
# it must be added as a function
def zfill(s, width):
    return '{:0>{w}}'.format(s, w=width)

# IO Expander Read data and store in sen_data
def fetchSensorData():
    # Read hexadecimal data and convert to binary
    data = "{0:b}".format(ord(i2c.read(0x38, 1)))
    # pad the data to 8 digits if necessary
    data = zfill(data, 8)
    # declare blo_data_dict as dictionary
    bol_data_dict = {}
    # Counter for the loop that enters the data from data into bol_data_dict
    bit_count = 7
    # Transfer data from data into bol_data_dict
    for i in data:
        if i == "0":
            bol_data_dict[bit_count] = False
            bit_count -= 1
        else:
            bol_data_dict[bit_count] = True
            bit_count -= 1
    # Transfer data to the global variable sen_data
    # bit 0 = SpeedLeft, bit 1 = SpeedRight, bit 2 = LineTrackerLeft,
    # bit 3 = LineTrackerMiddle, bit 4 = LineTrackerRight,
    # bit 5 = ObstclLeft, bit 6 = ObstclRight, bit 7 = Buzzer
    return bol_data_dict


# while loop that executes and displays showSensorData
# with an interval of one second
while True:
    sen_data = fetchSensorData()
    print("\n\nfrom the variable sen_data")
    print(sen_data)
    sleep(1000)
    print("\n\ndirectly from the function fetchSensorData()")
    print(fetchSensorData())
    sleep(1000)
