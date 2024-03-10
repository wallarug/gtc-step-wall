# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import board
import neopixel
import time
import busio
import digitalio

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 576
pixels_per_step = 31
start_pixel = 70        # Start pixels
num_steps = 16          # Number of steps

# starting DMX channel for offset
dmx_offset = 361 -1
dmx_number_channels = 48
dmx_values = [0] * dmx_number_channels

pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 0.5

# Serial
uart = busio.UART(board.GP8, board.GP9, baudrate=115200)

# Data LEDs
led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

# Hardcoded channels to pixels map.
channels_to_steps = {
    361: 1,  362: 1,  363: 1,  364: 2,  365: 2,  366: 2,
    367: 3,  368: 3,  369: 3,  370: 4,  371: 4,  372: 4,
    373: 5,  374: 5,  375: 5,  376: 6,  377: 6,  378: 6,
    379: 7,  380: 7,  381: 7,  382: 8,  383: 8,  384: 8,
    385: 9,  386: 9,  387: 9,  388: 10, 389: 10, 390: 10,
    391: 11, 392: 11, 393: 11, 394: 12, 395: 12, 396: 12,
    397: 13, 398: 13, 399: 13, 400: 14, 401: 14, 402: 14,
    403: 15, 404: 15, 405: 15, 406: 16, 407: 16, 408: 16,
}

print("Starting")

def update_pixels(channel):
    # work out step from the dictionary
    step = channels_to_steps[channel]

    # print("Step: ", step)

    # read the channel values from the dmx_values array
    r = dmx_values[(step - 1) * 3]
    g = dmx_values[(step - 1) * 3 + 1]
    b = dmx_values[(step - 1) * 3 + 2]

    # set the pixels
    set_pixels(step, r, g, b)

    # show the pixels
    pixels.show()
    
def update_all_pixels():
    # print("Step: ", step)
    for step in range(1, num_steps+1, 1):
        # read the channel values from the dmx_values array
        r = dmx_values[(step - 1) * 3]
        g = dmx_values[(step - 1) * 3 + 1]
        b = dmx_values[(step - 1) * 3 + 2]

        # set the pixels
        set_pixels(step, r, g, b)

    # show the pixels
    pixels.show()
    #print("Pixels Set!")

def set_pixels(step, r, g, b):
    """
    Set the color of pixels for a given step.
    """
    for i in range(pixels_per_step):
        pixel_index = start_pixel + ( (step - 1) * pixels_per_step) + i
        pixels[pixel_index] = (r, g, b)

def pixel_step_test():
    # For each step
    #  Set the 30 pixels
    for step in range(16):
        # the start pixel is start_pixel
        step_start = start_pixel + (31 * step)
        for pixel in range(31):
            i = step_start + pixel
            pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(2)


while True:
    #pixels.fill((0,0,0))
    #pixel_step_test()
    #continue

    data = uart.read(96)

    if data is not None:
        led.value = True
        data_string = ''.join([chr(b) for b in data])
        
        # check if we are dealing with the channel or the value
        first = True
        #print(data_string)
        for c in data_string:
            #print(ord(c))
            v = ord(c) + dmx_offset
            if ord(c) == 255 or ord(c) == 0:
                value = ord(c)
                previous = dmx_values[channel_index-1]
                if previous == value:
                    pass  # do nothing, the value is the same
                else:
                    # only update if changed
                    dmx_values[channel_index-1] = value
                first = True
                #channel_index = -1
                continue
            else:
                channel = ord(c)+dmx_offset
                channel_index = ord(c)
                first = False
                continue
        
        # update all the pixels once a full stream has been processed
        update_all_pixels()
        
        # fill in the pixels relevant for that channel (RGB)
        led.value = False

    # wait 100 ms before next read
    time.sleep(0.1)

    #pixels.fill((0,0,0))



def pixel_step_test():
    # For each step
    #  Set the 30 pixels
    for step in range(16):
        # the start pixel is start_pixel
        step_start = start_pixel + (31 * step)
        for pixel in range(31):
            i = step_start + pixel
            pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(5)

