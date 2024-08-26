# Import of the required modules
import microbit
import radio

# Switching on the radio hardware
radio.on()

# Definition of the variables for data transmission
data0 = "0"
data1 = "0"
data = "00"

# Query loop
while True:
    # read out the values of the acceleration sensor
    a = microbit.accelerometer.get_values()

    # Assign the letters to a direction and store in data0
    # micro:bit tilted to the left and not forward beyond the threshold value
    if a[0] >= 300 and a[1] <= 300:
        data0 = "l"
    # micro:bit tilted to the right and not forward beyond the threshold value
    elif a[0] <= -300 and a[1] <= 300:
        data0 = "r"
    # micro:bit tilted forward and not over threshold to the side
    elif a[1] <= -300 and a[0] >= -300 and a[0] <= 300:
        data0 = "f"
    # micro:bit tilted backwards
    elif a[1] >= 300:
        data0 = "b"
    # else 0
    else:
        data0 = "0"

# Assign the letters to a button and store in data1
    if microbit.button_a.is_pressed() == 1 and microbit.button_b.is_pressed() == 0:
        data1 = "a"
    elif microbit.button_a.is_pressed() == 0 and microbit.button_b.is_pressed() == 1:
        data1 = "b"
    elif microbit.button_a.is_pressed() == 1 and microbit.button_b.is_pressed() == 1:
        data1 = "c"
    else:
        data1 = "0"
    # combine data0 and data1 and store them in data
    data = data0 + data1
    # send data
    radio.send(data)
