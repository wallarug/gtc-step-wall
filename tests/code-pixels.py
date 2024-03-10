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

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 576

pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 0.1

while True:
    for i in range(num_pixels):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.05)
    time.sleep(1)
    pixels.fill((0,0,0))
    